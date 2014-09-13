#!/usr/bin/env python 
info="""
     """
__author__ = "ccwilliams" 
__date__   = "2014-09-12"

from LogConfig import get_logger
from stravalib import Client, unithelper
from filters import ActivityFilter
import pymysql as mdb
import traceback
import argparse
import datetime
import time

TIME_PAUSE   = 0.4 # in s, prevents max rate
LIMIT_SHORT  = 2700 # req per 15 min, 3 qps. thanks paul mach
DB_NAME      = "accts_and_apps" 
N_ACTIVITIES = 200 # number of activities to fetch for the athlete, some will
                   # be filtered based on activity type, private, manual upload, etc.
TABLES = { "apps":                "strava_apps", 
           "segment_ranks":       "strava_segment_ranks",
           "activity_to_segment": "activity_to_segment",
           "activities":          "strava_activities" }

conn = mdb.connect('localhost', 'root', '', DB_NAME, 
                   autocommit=True, charset="utf8") #non ascii 

#...............................................................................
# Input args
prsr = argparse.ArgumentParser(description=info, fromfile_prefix_chars="@")
prsr.add_argument("--athlete_ids", type=int, nargs="+",
                  help="Athletes to fetch activities for.")
prsr.add_argument("--access_tokens", type=str, nargs="+",
                  help="access_tokens for the athlete_id's in athlete_ids (mat"\
                       "ched indices if multiple) for the specified API app")
prsr.add_argument("--id_strava_app", type=int, default=102, # only app that works
                  help="The id for the app whose auth key to use in API calls")

#...............................................................................
# helpers
def get_user_activities(client, **kwargs):
    """Fetches user activities based a limit and kwargs
    """
    kwargs["ids"]      = True # only return ids
    kwargs["distance"] = 1    # min 1 mile
    acts     = client.get_activities(limit=N_ACTIVITIES)
    act_filt = ActivityFilter(acts, **kwargs)
    filtered = [ act for act in act_filt ]
    
    logger.info("returning %i/%i filtered summary activity ids" % \
        (len(filtered), 
         len(act_filt.filtered) + len(filtered)))

    return filtered

def add_activity(conn, athlete_id, Activity):
    """Adds an metrics from a DETAILED Activity object activity to the database
    """
    table     = TABLES["activities"]
    distance  = float( unithelper.miles(Activity.distance) )
    elevation = float( unithelper.feet(Activity.total_elevation_gain) )
    date_time  = Activity.start_date.strftime('%Y-%m-%d %H:%M:%S')

    statement = "INSERT INTO %s VALUES (%i, %i, '%s', '%s', %.2f, %.2f, '%s');" % \
                (table, athlete_id, Activity.id, Activity.type, Activity.name, \
		 distance, elevation, Activity.start_date)
    try:
        cur = conn.cursor()
        cur.execute(statement)
        logger.info("Activity %i added for athlete %i" % (Activity.id, athlete_id))

    except Exception, e:
        logger.critical("Error with activity %i for %i, error:\n%s" % (Activity.id, athlete_id, e))

    return

def add_segment_to_activity(conn, athlete_id, activity_to_segments):
    """Maps segment_ids to activity_ids for the specified athlete_id
    """
    table = TABLES["activity_to_segment"]

    for activity_id, segment_dict in activity_to_segments.items():
        logger.info("Adding %i segment_ids for athlete %i for activity %i" % \
            (len(segment_dict), athlete_id, activity_id))

        for segment_id in segment_dict.keys():
            statement = "INSERT INTO %s VALUES (%i, %i, %i);" % \
                        (table, athlete_id, activity_id, segment_id)
            try:
                cur = conn.cursor()
                cur.execute(statement)

            except Exception, e:
                logger.critical("Error with segment_id %i, error:/n%s" % \
                                (segment_id, e))
    return

def add_ranks(conn, athlete_id, activity_to_segments, segment_ranks):
    """Adds rank information to the db:
        auth_athlete_id, auth_athlete_rank, 
        other_athlete_id, other_athlete_rank,
        segment_id, segment_distance, segment_average_grade
    """
    table = TABLES["segment_ranks"]

    for activity_id, segment_dict in activity_to_segments.items():
       
        for segment_id, seg_info_dict in segment_dict.items():
            other_athlete_dict = segment_ranks[segment_id]["other_athletes"]
            auth_athlete_rank  = segment_ranks[segment_id]["auth_athlete_rank"]
            seg_dist           = seg_info_dict["distance"]
            seg_grade          = seg_info_dict["grade"]
            
            for other_athlete_id, other_athlete_rank in other_athlete_dict.items():
                statement = \
                    "INSERT INTO %s VALUES (%i, %i, %i, %i, %i, %.2f, %.2f);" % \
                    (table, 
                     athlete_id, auth_athlete_rank, 
                     other_athlete_id, other_athlete_rank, 
                     segment_id, seg_dist, seg_grade)

                try:
                    cur = conn.cursor()
                    cur.execute(statement)

                except Exception, e:
                    logger.critical("Error with rank statement:\n%s\nerror:%s" % \
                                    (statement, e))
    return

# main
def main():
    assert len(args.athlete_ids) == len(args.access_tokens)

    logger.info("app id: %i, fetching activities for ids %s" % \
                (args.id_strava_app, str(args.athlete_ids)))
    
    for i in range( len(args.access_tokens) ): # for each athlete
        client              = Client()
        client.access_token = args.access_tokens[i]
        athlete_id          = args.athlete_ids[i]
        
        # get summary activities first (filterd before detailed activity call)
        time.sleep(TIME_PAUSE)
        activity_ids = get_user_activities(client) 

        # now fetch detailed versions, add to db
        detailed_activites = []
        activity_to_segments = {} # { act_id: 
                                  #    { seg_id : 
                                  #       { "distance" : x, "grade" : y }, }, }

        segment_ranks = {}        # { seg_id : { "auth_athlete_rank" : auth_rank,
                                  #              "other_athletes"    : { other_id : other_rank, } } }
        for act_id in activity_ids:
	    try:
                 activity_to_segments[act_id] = {}

                 time.sleep(TIME_PAUSE)
            
                 detailed_activity = client.get_activity( act_id )
                 detailed_activites.append( detailed_activity )
		 
                 for seg_effort in detailed_activity.segment_efforts:
                     segment   = seg_effort.segment
                     seg_id    = int(segment.id)
                     seg_dist  = float( unithelper.miles(segment.distance) )
                     seg_grade = segment.average_grade
                     seg_dct   = { "distance" : seg_dist, "grade" : seg_grade }

                     activity_to_segments[act_id][seg_id] = seg_dct

                     if segment_ranks.has_key(seg_id): # already have ranks
                         continue                      # might be overlap between activities
                     else:
                         try: # some = hazardous = error
                             time.sleep(TIME_PAUSE) # now get ranks for this segment
                             leaderboard_entries = \
                                 client.get_segment_leaderboard(seg_id, 
                                                                top_results_limit=1).entries
                             segment_ranks[seg_id] = { "auth_athlete_rank" : -1,
                                                       "other_athletes" : {} }

                             for entry in leaderboard_entries:
                                 if entry.athlete_id == athlete_id: 
                                     segment_ranks[seg_id]["auth_athlete_rank"] = entry.rank
                                     continue
                            
                                 other_id   = entry.athlete_id
                                 other_rank = entry.rank
                                 segment_ranks[seg_id]["other_athletes"][other_id] = other_rank

                         except Exception, e:
                             logger.warning("Error with segment_id %i, removing from activity,"\
                                            " trace:\n %s" % (seg_id, traceback.print_exc()))
                             activity_to_segments[act_id].pop(seg_id)
                             continue
		 if len(activity_to_segments[act_id]) > 0:
                     add_activity(conn, athlete_id, detailed_activity) # if made it here, okay
		 else:
		     logger.info("No segments for activity %i, skipping" % act_id)

	    except Exception, e: # occurs with wrong privaleges, eg private activity
	        logger.warning("Error with activity %i for athlete %i, popping. tracebac:\n%s" % \
				(act_id, athlete_id, traceback.print_exc()))
		activity_to_segments.pop(act_id)

        # add all data to db
        add_segment_to_activity(conn, athlete_id, activity_to_segments)
        add_ranks(conn, athlete_id, activity_to_segments, segment_ranks)
        
    logger.info("Done.") 

if __name__ == "__main__":
    args   = prsr.parse_args()
    logger = get_logger(__file__)
    main()
