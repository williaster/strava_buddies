#!/Users/christopherwilliams/dotfiles/virtualenvs/.virtualenvs/lighttable/bin/python
info="""Adds user accounts to the strava_accts table in the accts_and_users 
        database
     """

__author__ = "ccwilliams"
__date__   = "2014-09-06"

import pymysql as mdb

NUM_ACCTS  = 100 # number of accounts to make
DB_NAME    = "accts_and_apps"
TABLE_NAME = "strava_accts"

def get_sql_statement(curr_num):
    """Generates the SQL statement for populating one row in the
       SQL table with account information
    """
    return "INSERT INTO %s VALUES ('%i', 'tim', 'green', 'ustas06+%i@hotmail.com', 'timgreen%i')" % \
           (TABLE_NAME, curr_num, curr_num, curr_num)

def show_table(conn):
    """Prints the contents of TABLE_NAME
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM %s" % TABLE_NAME)
    rows = cur.fetchall()
    for row in rows:
        print row
    return

#..............................................................................
# Script

# host, user, pw, db
conn = mdb.connect('localhost', 'root', '', DB_NAME)

with conn:
    cur = conn.cursor()

    print "Populating %s table in %s" % (TABLE_NAME, DB_NAME)
    for i in range(1, NUM_ACCTS + 1):
        if i == 1:
            print "example command: %s" % get_sql_statement(i)

        cur.execute( get_sql_statement(i) )

    show_table(conn)
    print "done!"
