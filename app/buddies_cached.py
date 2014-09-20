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
                              act_type="", as_options=True):
    """Fetches return_max user activities with distances >= min_distance for 
       the specified athlete. If act_type != "", will fetch the specified type only 
       ('Run' or 'Ride'). Returns as a dictoinary of items for use in dynamic html,
       or as the raw sql query
    """
    act_type = "AND activity_type = '%s'" % act_type if act_type else act_type

    statement = \
        "SELECT * FROM %s WHERE athlete_id = %i AND distance >= %i %s LIMIT %i;" \
        % (TABLES["activities"], athlete_id, min_distance, act_type, return_max)
    
    cur = conn.cursor()
    cur.execute(statement) 
    if as_options: 
        return get_activity_summaries( cur.fetchall() )
    else:
        return cur.fetchall()    

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


def get_candidate_buddies(conn, athlete_id, activity_ids, min_grade=0, min_distance=0.5): # CHANGED FROM 1!
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
    try:
        cand_buddies = [ tup[2] for tup in cur.fetchall() ]
        ctr_buddies  = Counter(cand_buddies), len(unique_segs)
        print "%i unique segments, %i unique candidate buddies of %i total pulled for " \
              "activities %s" % \
              (len(unique_segs), len(ctr_buddies[0]), len(cand_buddies), str(activity_ids))
    
    except Exception, e:
        print "error with ids: %s, 0 buddies returned, error:\n%s" % (activity_ids, e)
        ctr_buddies  = Counter(), len(unique_segs)

    return ctr_buddies

def get_data_for_athletes(conn, athlete_ids=[]):
    """Returns a pd.DF of all data columns for active users (run or ride ct > 0) 
       for the specified athlete_ids, and a separate DF for athlete metrics
       such as location/name/avatar url
       
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

def weighted_euclidean_similarity(other_athlete, curr_athlete, weights, 
                                  components=True):
    """Returns a Series of a composit as well as metric-wise similarity
       score based on the inverse of a weighted euclidean similarity.
    """
    delta  = other_athlete.ix["ride_count":"annual_dist_std"] - \
             curr_athlete.ix["ride_count":"annual_dist_std"]

    comps  =  weights*delta*delta 
    if components:
        result =  pd.Series([1/(1 + np.sqrt(comps.sum())), 
                     1/(1 + np.sqrt(comps[0])), 1/(1 + np.sqrt(comps[1])),
                     1/np.sqrt(comps[2:9].sum()), 
                     1/(1 + np.sqrt(comps[9])), 1/(1 + np.sqrt(comps[10]))],
                    index=["sim", "sim_ride", "sim_run", 
                           "sim_dowfreqs", "sim_dist", "sim_var"])
    else:
        result =  pd.Series([1/(1 + np.sqrt(comps.sum()))],
                            index=["sim"])
    return result

def get_weights(data, athlete_id):
  """Returns a numpy array of weights used in euclidean distance, 
     based on the athlete's run to ride ratio and giving equal weights
     to each day of the week.
  """
  w_ride = data.ix[athlete_id, "ride_count"] / \
           float(data.ix[athlete_id, "ride_count":"run_count"].sum())
  w_ride = min(w_ride, 0.95) # run counts for something
  w_run  = (1-w_ride) 

  weights = np.array([w_ride,w_run,0.143,0.143,0.143,0.143,0.143,0.143,0.143,1,0.5]) 
  return weights

def get_all_similarities(conn, all_data, all_ndata, athlete_id):
    """Computes similarity scores for all athletes in all_ndata vs
       the athlete with id = athlete_id. Handles removing the athlete from 
       the ndata df and returns the resulting df.
    """
    athlete_ndata      = all_ndata.ix[athlete_id, :]
    minusathlete_ndata = all_ndata.loc[all_ndata.index != athlete_id]
    weights            = get_weights(all_data, athlete_id)

    all_similarities = minusathlete_ndata.apply(weighted_euclidean_similarity, 
                                                axis=1, args=(athlete_ndata, weights),
                                                components=False)
    return all_similarities

def get_similarities(conn, athlete_id, friend_ids, candidate_buddy_ids):
    """Connects the logic for computing similarity scores between
       athlete_id vs thier friends and athlete_id vs candidate_buddy_ids
    """
    data, ndata, info = get_data_norm_data_athlete_info(conn)
    weights = get_weights(data, athlete_id)

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

    print final_buddies["sim"].min()

    result = { "n_candidates": n_candidates, # conversions for d3 data formatting
               "n_segments":   n_segs,
               "friends":      similarity_friends.to_json(),
               "user":         user_data.to_json(),
               "buddies":      final_buddies.T.to_dict().values(),
               "min_buddy_similarity":  final_buddies["sim"].min() }

    return result

def get_stats(conn, athlete_id, min_buddy_sim):
    """
    """
    friend_ids = get_athlete_connections(conn, athlete_id) 
    data, ndata, data_athlete_info = get_data_norm_data_athlete_info(conn)
    
    df_sim_all     = get_all_similarities(conn, data, ndata, athlete_id)
    df_sim_friends = df_sim_all.ix[friend_ids, :].dropna()

    fract_friends_lower = \
        df_sim_friends["sim"][ df_sim_friends["sim"] <  min_buddy_sim ].shape[0] / \
        float( df_sim_friends.shape[0] )

    fract_users_lower = \
        df_sim_all["sim"][ df_sim_all["sim"] <  min_buddy_sim ].shape[0] / \
        float( df_sim_all.shape[0] )

    print fract_friends_lower
    print fract_users_lower

    perc_friends_lower = "%2.0f" % (fract_friends_lower * 100)
    perc_users_lower   = "%2.0f" % (fract_users_lower   * 100)

    print perc_friends_lower
    print perc_users_lower

    return { "perc_friends_lower" : perc_friends_lower,
             "perc_users_lower":    perc_users_lower }


