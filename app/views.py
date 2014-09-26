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
MAX_BUDDIES  = 20
TABLE_APPS   = "strava_apps"
REDIRECT_URI = "http://127.0.0.1:5000/choose_authenticated"
AUTH_SCOPE   = None #"view_private" # None # none = public
app.secret_key = 'some_secret' # for flashes

cached_athletes = [ {"id": 1153632, "name" : "Chris W."},
                    {"id": 164890, "name"  : "Nicole O."},
                    {"id": 653, "name"     : "Rob M."},
                    {"id": 1744737, "name" : "David G." } ]

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

def get_conn():
    """Returns a pymysql connection object to the database.
    """
    return mdb.connect(user="root", host="localhost", 
                       db="accts_and_apps", charset='utf8')

#..............................................................................
# Views
@app.route('/')
@app.route('/index')
def index():
    """Home authentication page
    """ 
    conn = get_conn()
    client_id, client_secret = get_app_credentials(conn)
    client    = Client() # stravalib v3
    auth_link = client.authorization_url(client_id, REDIRECT_URI, scope=AUTH_SCOPE)
    title = "STRAVA buddies | Please log in to STRAVA"
    
    conn.close()
    return render_template("index.html", title=title, auth_link=auth_link,
                           tab="authenticate", examples=cached_athletes)

@app.route('/choose_examples', methods=["POST"])
def choose_example_activities():
    if "n_activities" in request.form.keys():
        n_activities = int(request.form["n_activities"])
    else:
        n_activities = 10

    athlete_id   = int(request.form["athlete_id"])
    athlete_name = [ dct["name"] for dct in cached_athletes if \
                     dct["id"] == athlete_id ][0]

    conn = get_conn() 
    activities = cbuds.get_user_activity_options(conn, athlete_id, n_activities)

    conn.close()
    return render_template("choose_activities.html", athlete_name=athlete_name,
                           activities=activities, athlete_id=athlete_id,
                           tab="choose", from_url="/choose_examples",
                           n_activities=n_activities)

@app.route('/choose_authenticated', methods=["GET", "POST"])
def choose_authenticated_activities():
    """Post-authentication, pre-buddy-suggestion
    """
    if request.args.get("error") == "access_denied":
        flash("Buddy suggestions cannot be made without authentication.")
        title = "Authentication error"
        return render_template("index.html", title=title, auth_link=auth_link)
    
    if False: # TODO: check that athlete is in DB
        return

    if "n_activities" in request.form.keys():
        n_activities = int(request.form["n_activities"])
    else:
        n_activities = 10

    conn         = get_conn() 
    code         = request.args.get("code")
    access_token = client.exchange_code_for_token(client_id,
                                                  client_secret,
                                                  code)
    client.access_token = access_token # now authorized for user
    athlete = client.get_athlete()
    athlete_name = athlete.firstname
    activities = buds.get_user_activity_options(client, n_activities)

    print access_token # makes easier to grab manually behind the scenes
    conn.close()
    return render_template("choose_activities.html", athlete_name=athlete_name, 
                           activities=activities, athlete_id=athlete.id,
                           tab="choose", from_url="/choose_authenticated",
                           n_activities=n_activities)

@app.route('/get_buddies', methods=["GET", "JSON"])
def get_buddies():
    athlete_id   = int( request.args["athlete_id"] )
    activity_ids = [] 
    for str_id in request.args.keys():
        try: 
            activity_ids.append( int(str_id) )
        except:
            continue

    conn = get_conn() 
    if request.args["from_url"] == "/choose_examples": # cached data
        result = cbuds.get_buddies_and_similarities(conn, athlete_id, 
                                                    activity_ids, MAX_BUDDIES)
    
    else: # need live api calls
        print "This feature is not implemented"
 
    conn.close()
    return jsonify( result )

@app.route('/get_buddy_stats', methods=["GET", "JSON"])
def get_stats():
    athlete_id    = int( request.args["athlete_id"] )
    min_buddy_sim = float( request.args["min_buddy_similarity"])
    
    conn = get_conn() 
    result = cbuds.get_stats(conn, athlete_id, min_buddy_sim)
    conn.close()
    return jsonify( result )

@app.route("/slides_wide", methods=["GET"])
def slides_wide():
    title="STRAVA buddies demo slides"
    return render_template("slides_wide.html", title=title)

@app.route('/yelp', methods=["GET"])
def yelp_over_n():
    """This is for hosting a yelp d3 project on this ec2 instance.
       williaster.com/yelp
    """
    return render_template("yelp_over_n.html")



