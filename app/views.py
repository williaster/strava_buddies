info="""Flask view mapping for the STRAVA buddies app
     """
__author__ = "ccwilliams"
__date__   = "20140909" # made

from flask import render_template, request, flash, jsonify
from stravalib.client import Client
import buddies as buds
import pymysql as mdb
from app import app
import pandas as pd

APP_ID       = 102 # which api account to use, 1-102
ACTIVITY_MAX = 10
TABLE_APPS   = "strava_apps"
REDIRECT_URI = "http://127.0.0.1:5000/choose_activities"
AUTH_SCOPE   = None #"view_private" # None # none = public
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
auth_link = client.authorization_url(client_id, REDIRECT_URI, scope=AUTH_SCOPE)

#..............................................................................
# Views
@app.route('/')
@app.route('/index')
def index():
    """Home authentication page
    """ 
    title     = "STRAVA buddies | Please log in to STRAVA"
    examples  = [ {"id":1, "name" : "Chris Williams"},
                  {"id":2, "name" : "Fake name" }]
    return render_template("index.html", title=title, auth_link=auth_link,
                           tab="authenticate", examples=examples)

@app.route('/examples_choose', methods=["POST"])
def choose_example_activities():
    print request.values
    print request.form
    print request.form["athlete_id"]
    activities = {}
    return render_template("choose_activities.html", athlete=athlete,
                           client=client, activities=activities,
                           tab="choose", examples=True)

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
    athlete = client.get_athlete()
    activities = buds.get_user_activity_options(client, ACTIVITY_MAX)

    print access_token # makes easier to grab manually behind the scenes
    return render_template("choose_activities.html", athlete=athlete, 
                           client=client, activities=activities, 
                           tab="choose", examples=False)

@app.route('/vis_get_test', methods=["GET"])
def vis_test():
    """Testing d3 visualization
    """
    buddies = pd.read_json("app/buddies_test.json", 
                           orient="index").to_json(orient="index")
    friends = pd.read_json("app/friend_sum_test.json", 
                           orient="records", typ="series").to_json()
    return jsonify(dict(buddies=buddies, friends=friends))


@app.route('/vis_empty', methods=["GET"]) 
def vis_empty():
    return render_template("vis_testing.html")
