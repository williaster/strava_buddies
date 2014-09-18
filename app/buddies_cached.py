#!/Users/christopherwilliams/dotfiles/virtualenvs/.virtualenvs/lighttable/bin/python
info="""Helper functions which manage the logic for buddy recommendations, with
        cached data (ie not through api calls)
     """

__author__ = "ccwilliams"
__date__   = "2014-09-13"

from scipy.spatial import distance
from collections import Counter
from dateutil import tz
import pymysql as mdb
import pandas as pd
import numpy as np
import filters 

TZ_LOCAL  = tz.tzlocal()
TABLES    = { "data":                "athletes_data",
              "friends":             "strava_friends",
              "segment_ranks":       "strava_segment_ranks",
              "activity_to_segment": "activity_to_segment",
              "activities":          "strava_activities" }

#...............................................................................
def get_user_activity_options(conn, athlete_id, return_max, min_distance=2, 
                              act_type=""):
    """Fetches return_max user activities with distances >= min_distance for 
       the specified athlete. If act_type != "", will fetch the specified type only 
       ('Run' or 'Ride')
    """
    act_type = "AND activity_type = '%s'" % act_type if act_type else act_type

    statement = \
        "SELECT * FROM %s WHERE athlete_id = %i AND distance >= %i %s LIMIT %i;" \
        % (TABLES["activities"], athlete_id, min_distance, act_type, return_max)
    
    cur = conn.cursor()
    cur.execute(statement) 
    return get_activity_summaries( cur.fetchall() )

def get_activity_summaries(sql_activity_query):
    """Pulls activity metrics and returns a dict with name, id, distance,
       elevation, type, and date.
    """
    summaries = []
    for activity in sql_activity_query:
        ath_id, act_id, act_type, act_name, \
            act_dist, act_elev, act_datetime = activity
        
        as_dct = { "id": act_id, "name": act_name, "type": act_type, 
                   "distance": act_dist, "elevation": act_elev, 
                   "date": act_datetime.replace(tzinfo=TZ_LOCAL).strftime("%m/%d") }
        summaries.append(as_dct)

    print "returning %i activities" % len(summaries)
    return summaries

def get_athlete_connections(conn, athlete_id, connection_type="friend"):
    """Returns a sequence of unique athlete_ids for the specified athlete_id of type  
       connection_type (friend, or follower)
    """
    statement = "SELECT DISTINCT friend_athlete_id FROM %s WHERE athlete_id = %i " \
                " AND type = '%s';" % \
                (TABLES["friends"], athlete_id, connection_type)
    cur = conn.cursor()
    cur.execute(statement)
    return [ id[0] for id in cur.fetchall() ]

def get_unique_segments_for_activities(conn, athlete_id, activity_ids):
    """Returns a sequence of unique segment_ids for the specified activity_ids
    """
    activity_ids = activity_ids if len(activity_ids) > 1 else [activity_ids[0], -1]

    statement = "SELECT DISTINCT segment_id FROM %s WHERE athlete_id = %i AND " \
                "activity_id IN %s;" % \
                (TABLES["activity_to_segment"], athlete_id, tuple(activity_ids)) 

    cur = conn.cursor()
    cur.execute(statement) 
    return [ seg_id[0] for seg_id in cur.fetchall() ]


def get_candidate_buddies(conn, athlete_id, activity_ids, min_grade=0, min_distance=1):
    """Returns a Counter mapping athlete_ids to the number of times they appeared in
       near the athlete rank in the segments for the specified athlete, for the specified
       activities, where activity segments are filtered for minimum grade and distance.
       nb: grade = %, distance = miles.
    """
    unique_segs = get_unique_segments_for_activities(conn, athlete_id, activity_ids)
    unique_segs = unique_segs if len(unique_segs) > 1 else [unique_segs[0], -1]

    statement = "SELECT auth_athlete_id, auth_athlete_rank, other_athlete_id " \
                "FROM %s WHERE auth_athlete_id = %i AND segment_id IN %s AND " \
                "other_athlete_rank > 1 AND segment_distance >= %.2f AND " \
                "segment_average_grade >= %.2f;" % \
                (TABLES["segment_ranks"], athlete_id, 
                    tuple(unique_segs), min_distance, min_grade)

    cur = conn.cursor()
    cur.execute(statement)
    cand_buddies = [ tup[2] for tup in cur.fetchall() ]
    ctr_buddies  = Counter(cand_buddies), len(unique_segs)

    print "%i unique segments, %i unique candidate buddies of %i total pulled for " \
          "activities %s" % \
          (len(unique_segs), len(ctr_buddies[0]), len(cand_buddies), str(activity_ids))
    return ctr_buddies

def get_data_for_athletes(conn, athlete_ids=[]):
    """Returns a pd.DF of all data columns for active users (run or ride ct > 0) 
       for the specified athlete_ids
       
       @param   athlete_ids   sequence of athlete ids, if empty returns all active users
    """
    athletes = "AND athlete_id IN %s" % \
               tuple(athlete_ids) if len(athlete_ids) > 0 else ""
    
    statement = "SELECT * FROM %s WHERE (run_count > 0 OR ride_count > 0) %s" % \
                (TABLES["data"], athletes)
    
    all_data  = pd.read_sql_query(statement, conn, index_col="athlete_id")
    data      = all_data.ix[:,"ride_count":"annual_dist_std"]
    info      = all_data[["first_name", "last_name", "city", "state", "avatar_url"]]

    return data, info 

def get_data_norm_data_athlete_info(conn):
    """Returns un-normalized and normalized (xrc-meanc / stdevc) DataFrames
       of activity metrics for all active athletes
    """
    data, athlete_info = get_data_for_athletes(conn, [])
    ndata = (data - data.mean()) / data.std()

    print "returning data for %i athletes" % data.shape[0]
    return data, ndata, athlete_info

def weighted_euclidean_similarity(other_athlete, curr_athlete, weights):
    """Returns a Series of a composit as well as metric-wise similarity
       score based on the inverse of a weighted euclidean similarity.
    """
    delta  = other_athlete.ix["ride_count":"annual_dist_std"] - \
             curr_athlete.ix["ride_count":"annual_dist_std"]

    comps  =  weights*delta*delta 
    result =  pd.Series([1/(1 + np.sqrt(comps.sum())), 
                         1/(1 + np.sqrt(comps[0])), 1/(1 + np.sqrt(comps[1])),
                         1/np.sqrt(comps[2:9].sum()), 
                         1/(1 + np.sqrt(comps[9])), 1/(1 + np.sqrt(comps[10]))],
                        index=["sim", "sim_ride", "sim_run", 
                               "sim_dowfreqs", "sim_dist", "sim_var"])
    return result

def get_similarities(conn, athlete_id, friend_ids, candidate_buddy_ids):
    """Connects the logic for computing similarity scores between
       athlete_id vs thier friends and athlete_id vs candidate_buddy_ids
    """
    data, ndata, info = get_data_norm_data_athlete_info(conn)
    w_run = data.ix[athlete_id, "ride_count"] / \
           (data.ix[athlete_id, "ride_count":"run_count"].sum())

    # Weigh run vs ride based on fraction of activities each constitutes for athlete
    # Weigh each day of the week as 1/7
    weights = np.array([w_run,1-w_run,0.143,0.143,0.143,0.143,0.143,0.143,0.143,1,0.5]) 
    
    athlete_ndata = ndata.ix[athlete_id, :]
    athlete_data  = data.ix[athlete_id, :]

    friend_ndata  = ndata.ix[friend_ids, :].dropna()
    buddy_ndata   = ndata.ix[candidate_buddy_ids, :].dropna()

    sim_friends   = friend_ndata.apply(weighted_euclidean_similarity, axis=1, #rows
                                       args=(athlete_ndata, weights))
    sim_buddies   = buddy_ndata.apply(weighted_euclidean_similarity, axis=1, #rows
                                      args=(athlete_ndata, weights))
    
    # combine together for visualization
    joined = sim_buddies.join( data.ix[candidate_buddy_ids, :].dropna() ).join(info)
    joined["athlete_id"] = joined.index.values
    joined["friend"]     = joined.apply(lambda row: row.athlete_id in friend_ids, axis=1)

    return sim_friends.median(), joined, athlete_data

def get_buddies_and_similarities(conn, athlete_id, activity_ids, max_buddies):
    """Returns all data needed for candidate buddy recommendation and visualization:
       #TODO
    """
    friend_ids      = get_athlete_connections(conn, athlete_id) 
    buddies, n_segs = get_candidate_buddies(conn, athlete_id, activity_ids) 
    buddy_ids       = buddies.keys()
    n_candidates    = len(buddy_ids)

    similarity_friends, \
    similarity_buddies, \
    user_data        = get_similarities(conn, athlete_id, friend_ids, buddy_ids)

    
    final_buddies = similarity_buddies.sort("sim", ascending=False)[:max_buddies]

    result = { "n_candidates": n_candidates, # conversions d3 data formatting
               "n_segments":   n_segs,
               "friends":      similarity_friends.to_json(),
               "user":         user_data.to_json(),
               "buddies":      final_buddies.T.to_dict().values() }

    return result

