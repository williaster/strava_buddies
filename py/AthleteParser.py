#!/Users/christopherwilliams/dotfiles/virtualenvs/.virtualenvs/lighttable/bin/python
info="""Parses the HTML for a Strava athlete HTML page to pull out interesting
        athlete metrics.
     """

__author__ = "ccwilliams"
__date__   = "2014-09-02"

from b4 import BeautifulSoup
import argparse
import pandas as pd

#...............................................................................
# Global vars


#...............................................................................
# Input arguments if script

#...............................................................................
# Classes

class AthleteParser(object):
    """Class representing a strava athlete
       Represented as a dataframe 
    """
    DAYS_OF_WEEK       = ["M", "T", "W", "Th", "F", "S", "S"] 
    CLASS_NUM_RUN_RIDE = "activity-breakdown"
    CLASS_ROW_CAL      = "activity-calendar"
    CLASS_ANNUAL_VIEW  = ""

    def __init__(self, html_str):
        self.strava_id   = strava_id
        self.doc         = get_doc(html_str)
        self.runs, \
            self.rides   = get_run_ride_ct()
                

    @staticmethod     
    def get_doc(file_or_url):
        """Returns the documenet root element for the input URL or file
        """
        return parse(file_or_url).getroot()

    def get_run_ride_ct(self):
        """Returns a dataframe containing the number of run and ride activities 
           for the athlete from the four-week dashboard, with days of the week 
           as columns
        """
        ct_div = self.doc.find_class()
        return 

    def get_avg_ct_dist_time(self):
        """Returns a data frame with "ride" and "run" rows and 4-week averages
           for "avg_ct", "avg_distance", "avg_time" as cols
        """
        return

    def get_annual_variability(self):
        """
        """
        return

    def find_annual_start(self):
        """Finds the first month from the yearly activity view where the 
           athlete has an activity
        """
        return


#...............................................................................
# 
