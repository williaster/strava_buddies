#!/usr/bin/env python 
info="""Spawns off several strava athete id probers with differen api accounts,
        and divides the athlete space among them
     """

__author__ = "ccwilliams"
__date__   = "2014-09-07"

from LogConfig import get_logger
import subprocess
import argparse
import random
import time
import os

TIME_BT_SPAWNS = [1, 4]
MAX_PER_PROBE  = 30000 # athletes to assign to a single prober
SCRIPT_SINGLE_PROBE = os.getcwd() + "/strava_athlete-id_prober.py"

#...............................................................................
# Args
prsr = argparse.ArgumentParser(description=info)
prsr.add_argument("id_api_min", type=int, 
                  help="Min value for an api id")
prsr.add_argument("id_api_max", type=int, 
                  help="Max value for an api id")
prsr.add_argument("id_athlete_min", type=int,
                  help="The min athlete id to probe, inclusive")
prsr.add_argument("id_athlete_max", type=int,
                  help="The max athlete id to probe, inclusive")
prsr.add_argument("-pp", "--per_probe", default=MAX_PER_PROBE, type=int,
                  help="Reqested per probe. The number of athlete ids assigned"\
                       " to each probe (depending on arguments, not all probes"\
                       " in supplied range will be used). Default: %i" % MAX_PER_PROBE)
prsr.add_argument("-d", "--dry", action="store_true",
                  help="If specified, will execute a dry run without spawning probers")

def main():
    if args.dry: logger.info("Dry run.")
    logger.info("Spawner, requested api range: %i - %i" % (args.id_api_min, args.id_api_max))
    logger.info("Requested athlete range: %i - %i" % (args.id_athlete_min, args.id_athlete_max))
    logger.info("Requested per probe: %i" % args.per_probe)
   
    # compute error handling for limits
    per_probe_needed = (args.id_athlete_max - args.id_athlete_min + 1.) / \
                       (args.id_api_max - args.id_api_min + 1. )
    
    if args.per_probe > MAX_PER_PROBE:
        logger.critical("Cannot assign probes more than %i athlete max! Exiting" \
                        % MAX_PER_PROBE)
        return
    
    if per_probe_needed > MAX_PER_PROBE:
        logger.critical("Required athletes per API (%.2f) exceeds max! Exiting" \
                        % per_probe_needed)
        return

    if per_probe_needed > args.per_probe:
        logger.critical("Per probe needed (%i) > per prob requested (%i)! Exiting" \
                        % (per_probe_needed, args.per_probe))
        return

    # Assign probes athlete ranges and start   
    curr_athlete_id_start = args.id_athlete_min # start athlete
    for curr_app_id in range(args.id_api_min, args.id_api_max + 1):

        # Check that we aren't over desired limit
        if curr_athlete_id_start > args.id_athlete_max:
            logger.warning("At/over desired athlete max (curr=%i), exiting " \
                           "without further API assignments!" % (curr_athlete_id_start))
            return
        
        curr_id_min = curr_athlete_id_start
        curr_id_max = min(curr_id_min + args.per_probe - 1, args.id_athlete_max)
        
        logger.info("Assigning app %i ids: %i - %i inclusive" % \
                    (curr_app_id, curr_id_min, curr_id_max)) 

        if not args.dry:
            subprocess.Popen( [SCRIPT_SINGLE_PROBE, 
                               str(curr_app_id), str(curr_id_min), str(curr_id_max)] )

        curr_athlete_id_start = curr_id_max + 1 # update 
        time.sleep( random.randint( TIME_BT_SPAWNS[0], TIME_BT_SPAWNS[1] ) ) 
   
    if curr_athlete_id_start - 1 < args.id_athlete_max:
        logger.warning("Final athlete assignment (%i) < requested (%i)" % \
                       (curr_athlete_id_start - 1, args.id_athlete_max))

    logger.info("All probes assigned, exiting.")

if __name__ == "__main__":
    args   = prsr.parse_args()
    logger = get_logger(__file__)
    main()
