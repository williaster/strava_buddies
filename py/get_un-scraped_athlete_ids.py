#!/Users/christopherwilliams/dotfiles/virtualenvs/.virtualenvs/lighttable/bin/python
info="""Pulls athlete_ids from the strava_ids table with cities that match a 
        those in a specified list and for which raw athlete page data do
        not exist. can over-write this filter behavior with options.
     """

__author__ = "ccwilliams"
__date__   = "2014-09-08"

from LogConfig import get_logger
import pymysql as mdb
import argparse

DB_NAME       = "accts_and_apps"
TABLE_IDS     = "strava_ids"
TABLE_SCRAPED = "athletes_raw"

CITIES    = ("san francisco",     # Cities to consider as Bay Area
             "san mateo",         # SQL query so set != better
             "sausalito",
             "belmont",
             "berkeley",
             "palo alto", 
             "los altos", 
             "daly city", 
             "south san francisco",
             "corte madera",
             "burlingame",
             "mill valley",
             "belvedere tiburon",
             "san bruno",
             "san carlos",
             "redwood city",
             "tamalpais-homestead valley",
             "richmond",
             "mountain view")

#...............................................................................
# args
prsr = argparse.ArgumentParser(description=info, fromfile_prefix_chars="@")
prsr.add_argument("outbase", type=str, 
                  help="base name for output file, include dir.")
prsr.add_argument("--skip", "-s", nargs="*", type=int,
                  help="Specify a list of athlete_ids to skip. Can supply "\
                       "from file with '@file'. If specified, overrides th"\
                       "e filtering based on the current scraped athlete table")

#...............................................................................
# functions
def get_ids(conn):
    """Retrieves athlete_id's from athlete city database if their city is in CITIES
    """
    statement = "SELECT id_athlete FROM %s WHERE city IN %s" % \
                (TABLE_IDS, str(CITIES))
    cur = conn.cursor() 
    cur.execute(statement)
    ids = cur.fetchall()
    
    logger.info("%i total athletes found" % len(ids))
    return [ id_tup[0] for id_tup in ids]

def get_scraped_ids(conn):
    """Pulls all athlete_ids for which raw data exist
    """
    statement = "SELECT athlete_id FROM %s" % TABLE_SCRAPED
    cur = conn.cursor() 
    cur.execute(statement)
    ids = cur.fetchall()
    
    logger.info("%i athletes have been scraped " % len(ids))
    return [ id_tup[0] for id_tup in ids]

def main():
    conn      = mdb.connect('localhost', 'root', '', DB_NAME, charset="utf8")
    if args.skip:
        logger.info("Manual id filter")
        filt_ids = set(args.skip)
    else:
        filt_ids = set(get_scraped_ids(conn))

    ids       = set(get_ids(conn))
    ids_final = ids - filt_ids

    f_name = "%s_ids-of-interest.athletes" % args.outbase
    if len(ids_final) > 0:
        with open(f_name, "w") as f_handle: # write to file
            for athlete_id in ids_final:
                f_handle.write("%i\n" % athlete_id)

            logger.info("%i filtered athlete_id's written to %s" % \
                        (len(ids_final), f_handle.name))
    else:
        logger.info("All athlete_id's filtered, no write.")

    return

if __name__ == "__main__":
    args   = prsr.parse_args()
    logger = get_logger(__file__)
    main()
