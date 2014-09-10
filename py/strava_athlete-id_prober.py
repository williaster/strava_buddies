#!/Users/christopherwilliams/dotfiles/virtualenvs/.virtualenvs/lighttable/bin/python
info="""
     """

__author__ = "ccwilliams" 
__date__   = "2014-09-07"

from LogConfig import get_logger
import pymysql as mdb
import argparse
import requests
import random
import json
import time
import os

LIMIT_LONG  = 30000 # req per day
LIMIT_SHORT = 600   # req per 15 min
PAUSE_SHORT = 15*60*60+1 # 15 min, in sec
TIME_BT_REQ = [1, 3]     # max = 1.5s / req

DB_NAME        = "accts_and_apps" 
TABLE_APPS     = "strava_apps"
TABLE_ATHLETES = "strava_ids"
APPS_PK        = "id_strava_app"
URL_API        = "http://www.strava.com/api/v3/"
STATUS_OK        = 0 # all good, atlete found
STATUS_NOT_FOUND = 1 # non-athlete
STATUS_EXCEED    = 2 # over limit
STATUS_LIM_SHORT = 3 # at short limit
STATUS_LIM_LONG  = 4 # at long limit

#...............................................................................
# Input args
prsr = argparse.ArgumentParser(description=info)
prsr.add_argument("id_strava_app", type=int,
                  help="The id for the app whose auth key to use in API calls")
prsr.add_argument("id_athlete_min", type=int,
                  help="Minimum athlete number to fetch (inclusive)")
prsr.add_argument("id_athlete_max", type=int,
                  help="Maximum athlete number to fetch (inclusive)")

#...............................................................................
# helpers
def get_access_token(conn, app_id):
    """Fetches and returns the access_token for the app with the specified ID
       from the strava apps table
    """
    statement = "SELECT access_token FROM %s WHERE %s = %i;" % \
                (TABLE_APPS, APPS_PK, app_id)
    #logger.info(statement)
    cur = conn.cursor()
    cur.execute(statement)
    return cur.fetchall()[0][0]

def check_status(response, athlete_id):
    """Checks the status of the response. Raises 
    """
    headers = response.headers
    text    = json.loads( response.text )
    usage   = get_usage(headers)
    status  = set()

    if "200" in headers["status"]: # okay
        status.add( STATUS_OK )
       
    elif "404" in headers["status"]: # no athlete
        status.add( STATUS_NOT_FOUND )

    elif "403" in headers["status"]: # limit exceeded
        status.add( STATUS_EXCEED )

    else:
        logger.warning("unknown status @athlete_id %i:\n\t: %s" % \
                       (athlete_id, headers))

    if usage["short"] >= LIMIT_SHORT:
        status.add( STATUS_LIM_SHORT )

    if usage["long"] >= LIMIT_LONG: # not mut. exclusive with short
        status.add( STATUS_LIM_LONG )
 
    return status, text, headers

def get_usage(headers):
    #logger.info(headers)
    u_short, u_long = headers["x-ratelimit-usage"].split(",")
    return { "short": int(u_short), "long": int(u_long) }

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
        logger.critical("Could not fetch access_token for app %i" % args.id_strava_app)
        raise 
   
    return conn, sesh, params

def get_city_state(response_text):
    """Fetches the city and state values for the athlete. In the case of
       an error (non-athlete), returns "NA", "NA"
    """
    try:
        city  = response_text["city"]
        state = response_text["state"]
    except:
        city, state = "NA", "NA"
    return city, state

def add_athlete_to_db(conn, id_athlete, city, state, id_strava_app):
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
    #dirs = get_out_dirs()

    for athlete_id in range(args.id_athlete_min, args.id_athlete_max + 1): #inclusive ]
        time.sleep( random.randint( TIME_BT_REQ[0], TIME_BT_REQ[1] ) )
        if athlete_id % 600 == 0:
            logger.info("curr athlete id: %i" % athlete_id)

        resp   = sesh.get("%sathletes/%i" % (URL_API, athlete_id), params=params)
        
        try:
            status, text, headers = check_status(resp, athlete_id)
        
        except Exception, e: # sometimes no usage in header
            logger.critical("Error with request, athlete %i. Skipping" % athlete_id)
            continue

        if (STATUS_OK in status) or (STATUS_NOT_FOUND in status):
            #outdir, city, state = pick_outdir(text, dirs)
            city, state = get_city_state(text)
            try:
                add_athlete_to_db(conn, athlete_id, city, state, args.id_strava_app)
            except:
                logger.critical("Could not add athlete %i, city/state: %s/%s" % \
                                (athlete_id, city, state))

        if (STATUS_EXCEED in status) or (STATUS_LIM_LONG in status):
            if (STATUS_LIM_LONG in status):
                logger.warning("Final status:\n\t%s" % status)
                logger.warning("Long-term status met/exceeded @athlete %i, exiting" %\
                               athlete_id)
                break

        if (STATUS_LIM_SHORT in status):
            logger.debug("Short term limit @athelete %i, pausing" % athlete_id)
            time.sleep( PAUSE_SHORT )
        
    logger.info("Done.") 

if __name__ == "__main__":
    args   = prsr.parse_args()
    logger = get_logger(__file__, args.id_strava_app)
    main()
