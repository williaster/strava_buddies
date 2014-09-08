from flask import render_template
from app import app
import pymysql as mdb

db = mdb.connect(user="root", host="localhost", 
				 db="world_innodb", charset='utf8')

# Views are defined as functions, decorators map these routes to the view
@app.route('/')
@app.route('/index')
def index():
    user = { 'nickname': 'Miguel' } # fake user
    return render_template("index.html",
        				   title = 'Home',
        				   user = user)

@app.route('/db')
def cities_page():
	with db: 
		cur = db.cursor()
		cur.execute("SELECT Name FROM City LIMIT 15;")
		query_results = cur.fetchall()
	
	# parse results
	cities = ""
	for result in query_results:
		cities += result[0]
		cities += "<br>"
	
	return cities
