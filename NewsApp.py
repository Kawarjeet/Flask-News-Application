from flask import Flask, jsonify, render_template, request, session, flash, redirect,abort 
from newsapi.articles import Articles
from newsapi.sources import Sources
#from flask.ext.socketio import SocketIO, emit
from sqlalchemy.orm import sessionmaker
import os
from tabledef import *
engine = create_engine('sqlite:///database.db', echo=True)

app = Flask(__name__)
a = Articles(API_KEY="867af1dffb80450b9770b4bcc10c8e14")
s = Sources(API_KEY="867af1dffb80450b9770b4bcc10c8e14")
"""app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@socketio.on('my event')                          # Decorator to catch an event called "my event":
def test_message(message):                        # test_message() is the event callback function.
    emit('my response', {'data': 'got it!'})      # Trigger a new event called "my response" 
 """                                                 # that can be caught by another callback later in the program.

@app.route("/")
def home():
	if session.get('logged_in'):
		return render_template("Welcome.html")
	else: 
		return render_template("login.html")

@app.route('/login',methods=["POST"])
def do_admin_login():
 
    POST_USERNAME = str(request.form['username'])
    POST_PASSWORD = str(request.form['password'])
 
    Session = sessionmaker(bind=engine)
    s = Session()
    query = s.query(User).filter(User.username.in_([POST_USERNAME]), User.password.in_([POST_PASSWORD]) )
    result = query.first()
    if result:
        session['logged_in'] = True
    else:
        flash('wrong password!')
    return home()

@app.route("/logout")
def logout():
    session['logged_in'] = False
    return home()

@app.route("/headlines")
def headlines():
	data =  a.get_by_latest("the-verge")
	article = data["articles"]
	#return jsonify(article)
	return render_template("Headlines.html",list=article,title="TOP HEADLINES")

@app.route("/general")
def general():
	data =  s.get_by_category("general")
	article = data["sources"]
	#return jsonify(data)
	return render_template("Display.html",list=article,title="GENERAL NEWS")

@app.route("/technical")
def tech():
	data = s.get_by_category("technology")
	article = data["sources"]
	return render_template("Display.html",list=article,title="TECHNICAL NEWS")

"""@app.route("/sports")
def sports():
	data = {
	'title': "SPORTS NEWS",
	'content': s.get_by_category("sport")

	}
	return jsonify(data)"""

@app.route("/business")
def business():
	data = s.get_by_category("business")
	article = data["sources"]
	return render_template("Display.html",list=article,title="BUSINESS NEWS")

@app.route("/entertainment")
def entertainment():
	data = s.get_by_category("entertainment")
	article = data["sources"]
	return render_template("Display.html",list=article,title="ENTERTAINMENT NEWS")

# @app.route("/science")
# def science():
# 	data = s.get_by_category("science-and-nature")
# 	article = data["sources"]
# 	return render_template("Display.html",list=article,title="SCIENCE AND NATURE NEWS")

"""@app.route("/gaming")#, methods=['POST'])
def gaming():
	data = {
	'title': "GAMING NEWS",
	'content': s.get_by_category("gaming")

	}
	return jsonify(data)"""


if __name__=='__main__':
	app.secret_key = os.urandom(12)
	app.run(host='0.0.0.0', debug=True)