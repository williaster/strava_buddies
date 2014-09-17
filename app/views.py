info="""Flask view mapping for the STRAVA buddies app
     """
__author__ = "ccwilliams"
__date__   = "20140909" # made

from flask import render_template, request, flash, jsonify
from stravalib.client import Client
import buddies as buds
import buddies_cached as cbuds
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
cached_athletes = [ {"id": 1153632, "name" : "Athlete 1"},
                    {"id": 164890, "name" : "Athlete 2"},
                    {"id": 653, "name" : "Athlete 3"},
                    {"id": 1744737, "name": "Athlete 4" } ]

#..............................................................................
# Views
@app.route('/')
@app.route('/index')
def index():
    """Home authentication page
    """ 
    title = "STRAVA buddies | Please log in to STRAVA"
    return render_template("index.html", title=title, auth_link=auth_link,
                           tab="authenticate", examples=cached_athletes)

@app.route('/choose_examples', methods=["POST"])
def choose_example_activities():
    print request.form
    print request.form["athlete_id"]

    athlete_id   = int(request.form["athlete_id"])
    athlete_name = [ dct["name"] for dct in cached_athletes if \
                     dct["id"] == athlete_id ][0]
    
    activities = cbuds.get_user_activity_options(conn, athlete_id, 10)

    return render_template("choose_activities.html", athlete_name=athlete_name,
                           client=client, activities=activities,
                           tab="choose", example="True")

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
    athlete_name = athlete.first_name
    activities = buds.get_user_activity_options(client, ACTIVITY_MAX)

    print access_token # makes easier to grab manually behind the scenes
    return render_template("choose_activities.html", athlete_name=athlete_name, 
                           client=client, activities=activities, 
                           tab="choose", example="False")

@app.route('/get_buddies', methods=["GET"])
def get_buddies():
    print request.args
    print request.args["example"]
    
    
    #print "ids:", activity_ids
    #print "type", type(activity_ids[0])

    return jsonify(dict(test={"t1":1}))

@app.route('/vis_get_test', methods=["GET"])
def vis_test():
    """Testing d3 visualization
    """
    buddies = pd.read_json("app/buddies_test.json", 
                           orient="index").T.to_dict().values()
    friends = pd.read_json("app/friend_sum_test.json", 
                           orient="records", typ="series").to_json()
    userData= pd.read_json("app/athlete_test.json",
                           orient="records", typ="series").to_json()

    return jsonify(dict(buddies=buddies, friends=friends, user=userData))


@app.route('/vis_empty', methods=["GET"]) 
def vis_empty():
    return render_template("vis_testing.html")
