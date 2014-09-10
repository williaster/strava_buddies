#!/usr/bin/env python
info="""Pulls the html from an athlete page with the specified strava 
        athlete_id, and stores in the raw scraping table
     """

__author__ = "ccwilliams"
__date__   = "2014-09-08"

import bs4
import time
import random
import requests 
import argparse
import pymysql as mdb
from LogConfig import get_logger
#from lxml.hmtl import fromstring

TIME_BT_REQ = [0.75,2] # randomize time between requests
PARAMS = { # required to authenticate a strava browser session, to view pages
    "utf8": None,
    "authenticity_token": None,
    "email"   : "ustas06@hotmail.com",
    "password": "tomgreen"
}

DB_NAME        = "accts_and_apps"
TABLE_SCRAPING = "athletes_raw"
TABLE_ATHLETES = "strava_ids"

#...............................................................................
# Input args
prsr = argparse.ArgumentParser(description=info, fromfile_prefix_chars="@")
prsr.add_argument("athlete_ids", nargs="*", type=int,
                  help="IDs for athletes whose athlete pages to visit")
prsr.add_argument("-ow", "--overwrite", action="store_true",
                  help="If specified, and this athletes site has been scraped "\
                       "previously, will overwrite the entry. Will abort by " \
                       "default")

#...............................................................................
# functions
def rand_float(start, end):
    return random.random() * (end - start) + start

def user_has_been_scraped(conn, athlete_id):
    """Checks database to see if the athlete_id is already present
    """
    statement = "SELECT 1 FROM %s WHERE athlete_id = %i" % \
                (TABLE_SCRAPING, athlete_id)
    cur = conn.cursor()
    return cur.execute(statement)

def add_raw_athlete(conn, athlete_id, raw_text):
    """Enters raw text blob into database for the specified athlete.
       nb: connection should have enabled autocommit.
    """
    statement = "INSERT INTO %s VALUES (%i, '%s', DEFAULT)" % \
                 (TABLE_SCRAPING, athlete_id, mdb.escape_string(raw_text))
    cur = conn.cursor()
    cur.execute(statement)
    return

def get_auth_cookies(sesh):
    """Authenticates session by logging in, returns the cookies to enable
       scraping several athlete pages
    """
    r_login = sesh.get("https://www.strava.com/login")
    soup    = bs4.BeautifulSoup(r_login.text) 

    try:
        PARAMS["utf8"] = \
            soup.find("input", {"name":"utf8"}).get("value").encode("utf-8")

        PARAMS["authenticity_token"] = \
            soup.find("input", {"name":"authenticity_token"}).get("value")
    
    except Exception, e:
        logger.critical("Error parsing login, exception:\n%s" % e)
        return False
    
    time.sleep( rand_float( TIME_BT_REQ[0], TIME_BT_REQ[1] ))
    r_session = sesh.post("http://www.strava.com/session", data=PARAMS)
    return r_session.cookies

def main():
    conn = mdb.connect('localhost', 'root', '', DB_NAME,
                       autocommit=True, charset="utf8") # non-ascii
    sesh    = requests.session()
    cookies = get_auth_cookies(sesh)
    
    if not cookies: return

    for athlete_id in args.athlete_ids:    

        has_been_scraped = user_has_been_scraped(conn, athlete_id)

        if has_been_scraped and not args.overwrite:
            logger.critical("Athlete %i has been scraped, exiting" % athlete_id)
            continue

        time.sleep( rand_float( TIME_BT_REQ[0], TIME_BT_REQ[1] ))
        r_athlete = sesh.get("http://www.strava.com/athletes/%i" % athlete_id, 
                             cookies=cookies)

        as_utf8 = r_athlete.text.encode("utf-8")

        try:
            add_raw_athlete(conn, athlete_id, as_utf8)
            logger.info("Scraped athlete %i" % athlete_id)
        except Exception, e:
            logger.critical("Failed to write raw page for athlete %i, error:\n%s" % \
                            (athlete_id, e))
            continue

if __name__ == "__main__":
    args   = prsr.parse_args()
    logger = get_logger(__file__)
    main()
