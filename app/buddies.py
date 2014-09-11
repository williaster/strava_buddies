#!/Users/christopherwilliams/dotfiles/virtualenvs/.virtualenvs/lighttable/bin/python
info="""Helper functions which manage the logic for buddy recommendations
     """

__author__ = "ccwilliams"
__date__   = "2014-09-10"

from stravalib import Client, unithelper
from LogConfig import get_logger
from dateutil import tz
import pymysql as mdb
import filters 

TZ_LOCAL = tz.tzlocal()
logger   = get_logger(__file__)

def get_user_activities(client, limit, **kwargs):
    """Fetches user activities based a limit and kwargs
    """
    filtered_summaries = []
    kwargs["id"] = True
    acts         = client.get_activities(limit=limit)
    for act in filters.ActivityFilter(acts, **kwargs):
        filtered_summaries.append( get_activity_summary(act) )
    
    return filtered_summaries

def get_detailed_activites(client, activity_ids):
    """Fetches detailed activities for the activity_ids provided
       #TODO It'd be cool to this in the background during act selection
    """
    return [ client.get_activity(id) for id in activity_ids ]

def get_unique_segments(detailed_activities):
    """Returns a dict of the following form, for the union of segments
       in the supplied activities
       {"ids": [ seg_ids ...], "segs": [ seg_objs ]}
       
       nb: seqs have matched indices
    """
    all_segs    = [ act.segment_effort for act in detailed_activities ]
    filt_unique = filters.filter_segment_efforts(all_segs, unithelper)
    result = { "ids" : [ seg.id for seg in filt_unique ],
               "segs": filt_unique }
    return result

def get_segment_leaderboard_ids(client, segment_ids):
    """Returns a 
       # TODO: change to sets once know how frequently you match in many segs
               remove ranks once check out
    """
    user_id = client.get_athlete().id
    result  = { "positive" : [] , "negative" : [], "ranks" : [] }
    for seg_id in segment_ids:
        entries = \
            client.get_segment_leaderboard(seg_id, top_results_limit=1).entries
       
        result["negative"].append( entries[0].athlete_id ) # 0 = rank 1
        for entry in entries[1:]: # user not in consistent order
            if entry.athlete_id == user_id:
                result["ranks"].append( entry.rank )
                continue
            
            result["positive"].append( entry.athlete_id )
    
    return result

def get_candidate_buddies():
    return

def get_activity_summary(activity):
    """Pulls activity metrics and returns an html <option> elment 
       with summary metric text and activity_id value
    """
    text = "%s, distance: %i miles (on %s)" % \
           (activity.name, 
            unithelper.miles(activity.distance),
            activity.start_date.replace(tzinfo=TZ_LOCAL).strftime("%m/%d"))
    
    opt = "<option value='%i'>%s</option>" % (text, activity.id)
    return opt

def get_user_friends():
    """
    """
    return



