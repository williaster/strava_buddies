"""Module for logging configuration
"""

__author__ = "ccwilliams"
__date__   = "2014-09-06"

import datetime
import logging
import os

def get_logger(filename, out_tail="", stream_lvl='INFO', write_lvl='DEBUG'):
    '''Analogous to logging.getLogger, returns a pre-formated logger object 
       which writes level 'stream' and higher to stdout and level 'write' to 
       file in 'outdir.' Stream format includes logger name, level, and message,
       File format includes the same plus date/time.

       @param   filename    __file__ for the current .py file
       @param   out_tail    Will be appended to the logger name if supplied       
       @param   stream_lvl  Level of severity, above which, will be written to
                            stdout
       @param   write_lvl   Ditto for writing to file
       @return  logging.getLogger() object
    '''
    NOW = datetime.datetime.now()
    d_lvls = {'DEBUG':logging.DEBUG, 
              'INFO':logging.INFO,
              'WARN':logging.WARN,
              'ERROR':logging.ERROR,
              'CRITICAL':logging.CRITICAL}
    try:
        stream_lvl = d_lvls[stream_lvl.upper()]
        write_lvl  = d_lvls[write_lvl.upper()]
    except:
        print 'Invalid stream/write_lvls, try: %s' % (str(d_lvls.keys()))
        raise

    trunc_file = filename.split("/")[-1][:-3]
    outdir     = "%s/logs/" % __file__[:-13]
    my_logger  = logging.getLogger('%s %s' % (filename, str(out_tail)))
    logging.basicConfig(level    = write_lvl,
                        format   = '%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                        datefmt  = '%m-%d %H:%M',
                        filename = '%s%s-%s-%s__%s%s.log' % \
                            (outdir, NOW.year, NOW.month, NOW.day, trunc_file, out_tail),
                        filemode = 'a')

    formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
    console   = logging.StreamHandler()
    console.setLevel(stream_lvl)
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)
    return my_logger
