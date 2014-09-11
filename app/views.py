info="""Flask view mapping for the STRAVA buddies app
     """
__author__ = "ccwilliams"
__date__   = "20140909" # made

from stravalib.client import Client
from flask import render_template, request, flash
from app import app
import pymysql as mdb
import buddies

APP_ID       = 102 # which api account to use, 1-102
TABLE_APPS   = "strava_apps"
REDIRECT_URI = "http://127.0.0.1:5000/choose_activities"
app.secret_key = 'some_secret' # for flashes
conn = mdb.connect(user="root", host="localhost", 
                   db="accts_and_apps", charset='utf8')

#..............................................................................
# Helpers
def get_app_credentials(conn):
    """Fetches and returns the client ID and 
    """
    statement = "SELECT client_id, client_secret FROM %s WHERE id_strava_app = %i;"\
                % (TABLE_APPS, APP_ID)
    cur = conn.cursor()
    cur.execute(statement)
    return cur.fetchall()[0]

client_id, client_secret = get_app_credentials(conn)
client    = Client() # stravalib v3
auth_link = client.authorization_url(client_id, REDIRECT_URI)

#..............................................................................
# Views
@app.route('/')
@app.route('/index')
def index():
    """Home authentication page
    """ 
    title     = "STRAVA buddies | Please log in to STRAVA"
    return render_template("index.html", title=title, auth_link=auth_link)

@app.route('/choose_activities')
def choose_activities():
    """Post-authentication, pre-buddy-suggestion
    """
    if request.args.get("error") == "access_denied":
        flash("Buddy suggestions cannot be made without authentication.")
        title = "Authentication error"
        return render_template("index.html", title=title, auth_link=auth_link)
    
    code         = request.args.get("code")
    access_token = client.exchange_code_for_token(client_id,
                                                  client_secret,
                                                  code)
    client.access_token = access_token # now authorized for user
    athlete    = client.get_athlete()

    print access_token # makes easier to grab manually behind the scenes
    return render_template("choose_activities.html", athlete=athlete, client=client, str=str)

@app.route('/buddies', methods=["POST"])
def buddies():
    """Display of athlete buddies
    """
    print request.form.getlist("activities")
    return render_template("buddies.html")

#..............................................................................
# Functions
def get_activities(self, before=None, after=None, limit=None):
    """
    """
    return

# filter activities



