#!/usr/bin/env python
info="""
     """

__author__ = "ccwilliams" 
__date__   = "2014-09-07"

from LogConfig import get_logger
from stravalib import client
import pymysql as mdb
import argparse
import random
import time

LIMIT_LONG  = 30000 # req per day
LIMIT_SHORT = 600   # req per 15 min
PAUSE_SHORT = 15*60*60+1 # 15 min, in sec

DB_NAME        = "accts_and_apps" 
TABLE_APPS     = "strava_apps"

#...............................................................................
# Input args
prsr = argparse.ArgumentParser(description=info, fromfile_prefix_chars="@")
prsr.add_argument("id_strava_app", type=int,
                  help="The id for the app whose auth key to use in API calls")
prsr.add_argument("athlete_ids", type=int, nargs="+"
                  help="Athletes to fetch friends for, must have authenticated" \
                       " the strava app corresponding to id_strava_app")
prsr.add_argument("aceess_tokens", type=str, nargs="+"
                  help="access_tokens for the athlete_id's in athlete_ids (mat"\
                       "ched indices if multiple) for the specified API app")
#...............................................................................
# helpers
def init():
    """Initializes the request session and fetches an access token for auth
    """
    conn = mdb.connect('localhost', 'root', '', DB_NAME, 
                       autocommit=True, charset="utf8") #non ascii 
    try: 
        sesh         = requests.session()
        access_token = get_access_token(conn, args.id_strava_app)
        params       = { "access_token" : access_token }
        #logger.info("params: %s" % params)
    except Exception, e:
        logger.critical("Could not fetch access_token for app %i" % \
                        args.id_strava_app)
        raise 
   
    return conn, sesh, params

def add_friend_to_db(conn, id_athlete, city, state, id_strava_app):
    """Adds athlete to the database
    """
    statement = "INSERT INTO %s VALUES (%i, '%s', '%s', %i, DEFAULT)" % \
                (TABLE_ATHLETES, id_athlete, city, state, id_strava_app)
    cur = conn.cursor()
    cur.execute(statement)
    return 

# main
def main():
    logger.info("app id: %i, athlete range: %i - %i" % \
                (args.id_strava_app, args.id_athlete_min, args.id_athlete_max))
    
    conn, sesh, params = init()

    logger.info("Done.") 

if __name__ == "__main__":
    args   = prsr.parse_args()
    logger = get_logger(__file__, args.id_strava_app)
    main()
