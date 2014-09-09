#!/Users/christopherwilliams/dotfiles/virtualenvs/.virtualenvs/lighttable/bin/python
info="""Parses the HTML for a Strava athlete HTML page to pull out interesting
        athlete metrics.
     """

__author__ = "ccwilliams"
__date__   = "2014-09-02"

import numpy as np
import warnings
import bs4
import re

warnings.filterwarnings('error') # catch div by zero in freq by day calculation

#...............................................................................
# Global vars
MI_PER_KM = 0.621

#...............................................................................
# Classes
class AthleteParser(object):
    """Class representing a strava athlete, methods enable parsing raw athlete
       pages
    """
    def __init__(self, athlete_id, raw_html):
        self.athlete_id  = athlete_id
        self.soup        = bs4.BeautifulSoup(raw_html)
        self.run_ct      = self.get_run_ct()
        self.ride_ct     = self.get_ride_ct()
        self.frequencies = self.get_freq_by_day()
        self.distance_median, self.distance_std = \
            self.get_annual_dist_median_std_dev()

        print "median", self.distance_median
        print "std", self.distance_std
        print "mi-per-px", self.get_mi_per_px()
        print "run-ct", self.run_ct
        print "ride-ct", self.ride_ct
        print "freqs", self.frequencies
        

    def get_run_ct(self):
        """
        """
        run_icon = self.soup.select(".activity-breakdown .icon-run")[0]
        run_ct   = int( run_icon.previous_sibling.previous_sibling.text )
        return run_ct

    def get_ride_ct(self):
        """
        """
        ride_icon = self.soup.select(".activity-breakdown .icon-ride")[0]
        ride_ct   = int( ride_icon.previous_sibling.previous_sibling.text )
        return ride_ct

    def get_freq_by_day(self):
        rows = self.soup.select(".activity-calendar .row")[1:-1] #  0 = headers
                                                                 # -1 = variable
        result = np.empty(shape=(3,7)) # no div by zero, 'pseudo ct'

        for i in range( len(rows) ): # for each week
            all_days  = rows[i].select(".day")
        
            #highlighted = activity
            activity_days = set( rows[i].select(".highlighted") )
        
            # boolean list for where activities occurr
            result[i] = [ day in activity_days for day in all_days ]
       
        try: 
            return result.sum(axis=0) / result.sum()
        except Warning:
            return np.array([0 for i in range(7)])

    def get_mi_per_px(self):
        """Returns the scale for the annual distance per week interval,
           in miles per px or computing distances from element px
        """
        get_px    = lambda tick: int( re.findall("[a-z:]*([\d]+)px", 
                                                 tick.get("style"))[0] )
        yaxis     = self.soup.select("ul.y-axis")[0]
        two_ticks = yaxis.findChildren()[:2]
        adj_units = MI_PER_KM if "km" in two_ticks[0].text else 1 # store 1 unit

        delta_mi  = int( two_ticks[1].text ) * adj_units # tick 1 = 0
        delta_px  = ( get_px(two_ticks[1]) - get_px(two_ticks[0]) )

        return delta_mi / float(delta_px)

    def get_annual_distances(self, ivals, mi_per_px):
        """Returns a numpy array of weekly intervals in mi, for the year
           as well as the first non-zero index for subsequent computations
        """
        dists        = np.array([ self.get_ival_distance(ival, mi_per_px) \
                                  for ival in ivals ])
        idx_non_zero = np.argmax( dists > 0 ) #
        return dists, idx_non_zero

    def get_ival_distance(self, ival, mi_per_px):
        """Returns the distance in mi for a single distance interval
        """
        try: 
            ival_bar = ival.select("div.fill")[0]
        except: # no bar
            return 0
    
        get_px   = lambda bar: int(re.findall("[a-z:]*([\d]+)px", 
                                              bar.get("style"))[0])
        px_dist  = get_px(ival_bar)
        return mi_per_px * px_dist

    def get_annual_dist_median_std_dev(self):
        """Computes the annual activity (does not distinguish run vs ride)
           distance median and standard deviation in mi, starting from the first
           logged activity this year
        """
        weekly_ivals        = self.soup.select("li.interval")[:-1] # last = filler
        mi_per_px           = self.get_mi_per_px()
        dists, idx_non_zero = self.get_annual_distances(weekly_ivals, mi_per_px)
        print "dists", dists 
        print "1st non-zero idx", idx_non_zero
        return np.median(dists[idx_non_zero:]), np.median(dists[idx_non_zero:])

#...............................................................................
# 
