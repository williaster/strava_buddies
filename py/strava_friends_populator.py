#!/usr/bin/env python 
info="""Adds friends and followers for the supplied athlete_ids to a DB.
        Purpose of having athlete-specific access tokens is more complete
        access.
     """
__author__ = "ccwilliams" 
__date__   = "2014-09-12"

from LogConfig import get_logger
from stravalib import Client
import pymysql as mdb
import argparse
import time

TIME_PAUSE    = 0.4 # in s, prevents max rate
LIMIT_SHORT   = 2700 # req per 15 min, 3 qps. thanks paul mach
DB_NAME       = "accts_and_apps" 
TABLE_APPS    = "strava_apps"
TABLE_FRIENDS = "strava_friends"
conn = mdb.connect('localhost', 'root', '', DB_NAME, 
                   autocommit=True, charset="utf8") #non ascii 

#...............................................................................
# Input args
prsr = argparse.ArgumentParser(description=info, fromfile_prefix_chars="@")
prsr.add_argument("athlete_ids", type=int, nargs="+",
                  help="Athletes to fetch friends for, must have authenticated" \
                       " the strava app corresponding to id_strava_app")
prsr.add_argument("aceess_tokens", type=str, nargs="+",
                  help="access_tokens for the athlete_id's in athlete_ids (mat"\
                       "ched indices if multiple) for the specified API app")
prsr.add_argument("--id_strava_app", type=int, default=102, # only app that works
                  help="The id for the app whose auth key to use in API calls")
#...............................................................................
# helpers
def add_friends_to_db(conn, athlete_id, friend_ids, type):
    """Adds athlete to the database
    """
    for id in friend_ids:
        try:
            statement = "INSERT INTO %s VALUES (%i, %i, '%s')" % \
                        (TABLE_FRIENDS, athlete_id, id, type)
            cur = conn.cursor()
            cur.execute(statement)
            logger.info("%i added as %s for athlete %i" % \
                        (id, type, athlete_id))

        except Exception, e:
            logger.critical("Error for friend %i of %i, error:\n%s" % \
                            (athlete_id, id, e))
     
# main
def main():
    assert len(args.athlete_ids) == len(args.access_tokens)

    logger.info("app id: %i, fetching friends for ids %s" % \
                (args.id_strava_app, str(args.athlete_ids)))
    
    for i in len(args.access_tokens):
        client              = Client()
        client.access_token = args.access_tokens[i]
        athlete_id          = args.athlete_ids[i]


        time.sleep(TIME_PAUSE)
        friends   = [ friend.id for friend in client.get_athlete_friends() ]
        time.sleep(TIME_PAUSE)
        followers = [ follower.id for follower in client.get_athlete_followers() ]

        add_friends_to_db(conn, athlete_id, friends,   type="friend")
        add_friends_to_db(conn, athlete_id, followers, type="follower")
        
    logger.info("Done.") 

if __name__ == "__main__":
    args   = prsr.parse_args()
    logger = get_logger(__file__)
    main()
