#!/Users/christopherwilliams/dotfiles/virtualenvs/.virtualenvs/lighttable/bin/python
info="""Helper functions which manage the logic for buddy recommendations
     """

__author__ = "ccwilliams"
__date__   = "2014-09-10"

from stravalib import Client, unithelper
from scipy.spatial import distance
#from LogConfig import get_logger
from dateutil import tz
import pymysql as mdb
import numpy as np
import filters 

TZ_LOCAL  = tz.tzlocal()
SEG_LIMIT = 500 # max numbr of segments to pull, to avoid exceeding api limits
                # TODO: turn this into a counter?
#logger   = get_logger(__file__)

def get_candidate_buddies(client, activity_ids):
    """Wraps all of the logic for obtaining a list of candidate buddy
       athlete_ids from a sequence of activity_id's. Order of events:
            1. Pull detailed Activity objects for specified ids
            2. Pulls segment's from Activity SegmentEffort objects, filters 
               segments based on distance and grade, and unions all 
               resultant segment_id's.
            3. Fetches leaderboards for all filtered segment_id's
            4. Fetches a dict of of sequences of candidate buddy athlete_id's
               and negative control athlete_id's (which come from the top of
               the leaderboard)
       
       Max number of candidate buddies returned = unique_segs * 4
       Max number of negative controls returned = unique_segs * 1

       nb: assumes activity_id's have already been filtered for REAL
           activities (i.e., not manual uploads, etc.)

       returns dict of id's and of the segments used
    """
    detailed_activities = get_detailed_activites(client, activity_ids)
    unique_segs         = get_unique_segments(detailed_activities)
    ids = get_segment_leaderboard_ids(client, unique_segs["ids"])
    return ids, unique_segs


def get_user_activity_options(client, return_max, **kwargs):
    """Fetches user activities based a limit and kwargs
    """
    filtered_summaries = []
    kwargs["id"] = True
    acts         = client.get_activities(limit=100)
    act_filt     = filters.ActivityFilter(acts, **kwargs)
    for act in act_filt:
        filtered_summaries.append( get_activity_summary(act) )
    
    print "%i/%i filtered summary activities, returning %i" % \
        (len(filtered_summaries), len(act_filt.filtered), 
         min(return_max, len(filtered_summaries)))

    return filtered_summaries[:return_max]

def get_detailed_activites(client, activity_ids):
    """Fetches detailed activities for the activity_ids provided
       #TODO It'd be cool to this in the background during act selection
    """
    print "Fetching %i detailed activities" % len(activity_ids)
    return [ client.get_activity(id) for id in activity_ids ]

def get_unique_segments(detailed_activities):
    """Returns a dict of the following form, for the union of segments
       in the supplied activities
       {"ids": [ seg_ids ...], "segs": [ seg_objs ]}
       
       nb: seqs have matched indices
    """
    all_seg_efforts = []
    for act in detailed_activities:
        all_seg_efforts.extend( act.segment_efforts )

    filt_unique     = filters.filter_segment_efforts(all_seg_efforts, unithelper)
    result          = { "ids" : [ seg.id for seg in filt_unique ],
                        "segs": filt_unique }
    
    print "Returning %i/%i filtered unique segments" % \
        (len(filt_unique), len(all_seg_efforts))
    return result

def get_segment_leaderboard_ids(client, segment_ids):
    """Returns a 
       # TODO: change to sets once know how frequently you match in many segs
               remove ranks once check out
    """
    user_id = client.get_athlete().id
    result  = { "positive" : [] , "negative" : [], "ranks" : [] }

    if len(segment_ids) > SEG_LIMIT: # sample so don't exceed limit
        segment_ids = np.random.choice(segment_ids, 
                                       size=SEG_LIMIT, replace=False)
    for seg_id in segment_ids:
        try:
            entries = \
                client.get_segment_leaderboard(seg_id, top_results_limit=1).entries
        except Exception, e:
            print "Error with segment_id %i, error: %s" % (seg_id, e)
            continue
       
        result["negative"].append( entries[0].athlete_id ) # 0 = rank 1
        for entry in entries[1:]: # user not in consistent order
            if entry.athlete_id == user_id:
                result["ranks"].append( entry.rank )
                continue
            
            result["positive"].append( entry.athlete_id )
    
    print "Returning %i positive and %i negative athlete_id's" % \
                (len(result["positive"]), len(result["negative"]))
    return result

def get_activity_summary(activity):
    """Pulls activity metrics and returns a dict with id, distance,
       elevation, and date.
    """
    vals = { "id": activity.id, "name": activity.name, 
             "distance": unithelper.miles(activity.distance),
             "elevation": unithelper.feet(activity.total_elevation_gain), 
             "date": activity.start_date.replace(tzinfo=TZ_LOCAL).strftime("%m/%d") }
    return vals

def get_user_connection_ids(client, following=True, followers=True):
    """Returns the set of athlete_id's of the athletes the authenticated athlete
       is either following or who are following the user, depending on params
    """
    connection_ids = set()
    if following:
        for friend in client.get_athlete_friends():
            connection_ids.add( friend.id)
    
    if followers:
        for follower in client.get_athlete_followers():
            connection_ids.add( follower.id )

    print "Returning %i connection athlete_id's" % len(connection_ids)
    return connection_ids


