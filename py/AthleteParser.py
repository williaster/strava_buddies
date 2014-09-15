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
class Athlete(object):
    """Class representing a strava athlete, methods enable construction from
       raw athlete html pages or from a database entry
    """

    @classmethod
    def from_html(cls, athlete_id, raw_html, logger):
        """Returns an athlete from a raw strava athlete html page
        """
        obj = Athlete()
        obj.athlete_id       = athlete_id
        obj.logger           = logger
        obj.soup             = bs4.BeautifulSoup(raw_html)
        obj.first_name, \
            obj.last_name    = obj.get_name()
        obj.city, \
            obj.state        = obj.get_location()
        obj.run_count        = obj.get_run_count()
        obj.ride_count       = obj.get_ride_count()
        obj.frequencies      = obj.get_freq_by_day()
        obj.distance_median, \
            obj.distance_std = obj.get_annual_dist_median_std_dev()
        obj.avatar_url       = obj.get_avatar_url()

        return obj
        """
        print "first", obj.first_name
        print "last", obj.last_name
        print "city", obj.city
        print "state", obj.state
        print "median", obj.distance_median
        print "std", obj.distance_std
        print "run-ct", obj.run_count
        print "ride-ct", obj.ride_count
        print "freqs", obj.frequencies
        print "mi-per-px", obj.get_mi_per_px()
        print "avatar-url", obj.avatar_url
        """

    @classmethod
    def from_sql(cls, sql_vals, logger):
        """Returns an athlete from a single MySQL row
        """
        obj = Athlete()
        obj.logger          = logger
        obj.athlete_id      = sql_vals[0]
        obj.first_name      = sql_vals[1]
        obj.last_name       = sql_vals[2]
        obj.city            = sql_vals[3]
        obj.state           = sql_vals[4]
        obj.ride_count      = sql_vals[5]
        obj.run_count       = sql_vals[6]
        obj.frequencies     = np.array( sql_vals[7:14] )
        obj.distance_median = sql_vals[14]
        obj.distance_std    = sql_vals[15]
        obj.avatar_url      = sql_vals[16]

        return obj

    @classmethod
    def athletes_df_from_sql(cls):
        """
        """
        import pandas as pd
        return

    def get_name(self):
        """Fetches the athlete's first and last name, encodes as utf8 for
           non-ascii characters
        """
        try:
            first, last = re.findall("([\w ]+) ([\w]+)", 
				     self.soup.select("title")[0].text.split("|")[0])[0]
        except Exception, e:
            self.logger.error("Error fetching name")
            raise
        return first.encode("utf-8"), last.encode("utf-8")

    def get_location(self):
        """Fetches athlete city and state, encodes as utf8 for non-ascii chars
        """
        try:
            #city, state = self.soup.select("p.location")[0].text.split(",")
            location    = self.soup.select("p.location")[0].text
            city, state = re.findall("([ \d\w']*), ([ \d\w',]*)", location)[0]
        except Exception, e:
            self.logger.error("Error fetching location")
            raise
        return city.encode("utf-8"), state.strip().encode("utf-8")


    def get_run_count(self):
        """Fetches the 4-week run count
        """
        try:
            run_icon  = self.soup.select(".activity-breakdown .icon-run")[0]
            run_count = int( run_icon.previous_sibling.previous_sibling.text )
        except Exception, e:
            self.logger.error("Error fetching run ct")
            raise
        return run_count

    def get_ride_count(self):
        """Fetches the 4-week ride count
        """
        try:
            ride_icon  = self.soup.select(".activity-breakdown .icon-ride")[0]
            ride_count = int( ride_icon.previous_sibling.previous_sibling.text )
        except Exception, e:
            self.logger.error("Error fetching ride ct")
            raise
        return ride_count

    def get_freq_by_day(self):
        """Computes athlete activity frequency by day of the week,
           based on the first 3 of 4 weekly activity breakdowns
        """
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
            return result.sum(axis=0) / float( result.sum() )
        except Warning:
            return np.array([0 for i in range(7)]) # zero div = no activities

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
        print dists
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
        weekly_ivals        = self.soup.select("li.interval")
        mi_per_px           = self.get_mi_per_px()
        dists, idx_non_zero = self.get_annual_distances(weekly_ivals, mi_per_px)
        #print "dists", dists 
        #print "1st non-zero idx", idx_non_zero
        return np.median(dists[idx_non_zero:]), np.std(dists[idx_non_zero:])

    def get_avatar_url(self):
        """Fetches url for athlete avatar
        """
        avatar = self.soup.select("div.avatar-xl")[0]
        img    = avatar.select("img")[0]
        return img.get("src")

    def add_athlete_data(self, conn, table):
        """Inserts athlete values
           Raises any exceptions that occur (so client should handle)
        """
        statement = \
        'INSERT INTO %s VALUES ' \
        '(%i,"%s","%s","%s","%s",'\
        ' %i,%i,%.3f,%.3f,%.3f,%.3f,%.3f,%.3f,%.3f,%.1f,%.1f,"%s")'\
         % (table,
            self.athlete_id,
            self.first_name, self.last_name,
            self.city, self.state,
            self.ride_count, self.run_count,
            self.frequencies[0], self.frequencies[1], self.frequencies[2],
            self.frequencies[3], self.frequencies[4], self.frequencies[5],
            self.frequencies[6], 
            self.distance_median, self.distance_std, self.avatar_url)

        #print statement
        cur = conn.cursor()
        cur.execute(statement)
        self.logger.info("athlete %i parsed" % self.athlete_id)
        return 

    

#...............................................................................
# 
