#!/Users/christopherwilliams/dotfiles/virtualenvs/.virtualenvs/lighttable/bin/python
info="""Parses raw athlete html pages from the athletes_raw table and
        adds the parsed data to the athletes_data table. Parses only raw entries
        that don't have a corresponding athlete_id in the athletes_data table
     """

__author__ = "ccwilliams"
__date__   = "2014-09-08"

from LogConfig import get_logger
from AthleteParser import Athlete
import pymysql as mdb
import argparse

DB_NAME        = "accts_and_apps"
TABLE_SCRAPING = "athletes_raw"
TABLE_PARSED   = "athletes_data"

#...............................................................................
# Input args
prsr = argparse.ArgumentParser(description=info)
#prsr.add_argument("athlete_ids", nargs="*", type=int,
#                  help="IDs for athletes whose athlete pages to visit")
#prsr.add_argument("-ow", "--overwrite", action="store_true",
#                  help="If specified, and this athletes site has been scraped "\
#                       "previously, will overwrite the entry. Will abort by " \
#                       "default")

#...............................................................................
# functions

def get_raw_athlete_page(conn, athlete_id):
    """Fetches raw strava athlete page for the specified athlete from the db
    """
    statement = "SELECT page FROM %s WHERE athlete_id =  %i;" % \
                 (TABLE_SCRAPING, athlete_id)
    cur = conn.cursor()
    cur.execute(statement)
    raw = cur.fetchall()
    return raw[0][0] # tuple of results, tuple for value

def get_unparsed_athlete_ids(conn):
    """Fetches athlete_id's from the athletes_raw table which don't have entries
       in the atheletes_data table
    """
    statement = "SELECT athlete_id FROM %s WHERE athlete_id NOT IN "\
                "(SELECT athlete_id FROM %s);" % (TABLE_SCRAPING, TABLE_PARSED)
    cur = conn.cursor()
    cur.execute(statement)
    ids = cur.fetchall()
    return ids

def retrieve_athlete(conn, athlete_id):
    """Retrieves athlete data from table and initializes an Athlete obj
       (for testing)
    """
    statement = "SELECT * FROM %s WHERE athlete_id = %i" % \
                (TABLE_PARSED, athlete_id)
    cur = conn.cursor()
    cur.execute(statement)
    as_sql  = cur.fetchall()[0]
    return Athlete.from_sql( as_sql, logger )

def main():
    conn = mdb.connect('localhost', 'root', '', DB_NAME,
                       autocommit=True, charset="utf8") # non-ascii
    unparsed_ids = get_unparsed_athlete_ids(conn)

    logger.info("Parsing %i athletes pages..." % (len(unparsed_ids)))
    for athlete_id_tup in unparsed_ids:
        athlete_id = athlete_id_tup[0] 
        raw_page   = get_raw_athlete_page(conn, athlete_id)

        try: athlete = Athlete.from_html(athlete_id, raw_page, logger)
        
        except Exception, e:
            logger.critical("Error parsing athlete %i, error:\n%s" % \
                            (athlete_id, e))
            continue

        try: 
            athlete.add_athlete_data(conn, TABLE_PARSED)

            athlete2 = retrieve_athlete(conn, athlete_id)

            print { k: v for (k,v) in athlete.__dict__.items() if k != "soup" }
            print athlete2.__dict__
            

        except Exception, e:
            logger.critical("Error writing athlete %i to DB, error:\n%s" % \
                            (athlete_id, e))
            continue

if __name__ == "__main__":
    args   = prsr.parse_args()
    logger = get_logger(__file__)
    main()
