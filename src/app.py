# This is the main app script for flask that will handles requests to the webpage

import os                 # used to get environment variables so we don't store passwords
# python web-framework
from flask import (
    Flask,
    redirect,
    url_for,
    request,
    make_response,
    render_template
)
import mysql              # mysql connector library
import sqlalchemy as sql  # sqlalchemy is used to connect to db
import pandas as pd       # used to execute SQL statements on sqlalchemy engine
import sha3               # cryptographic hash for user verification
from markupsafe import escape

# SET ENVIRONMENT VARIABLES FOR DB
# since this will be run at the same location as DB these are formatted for local connections to DB
host = "127.0.0.1"  # localhost
port = 3306         # local port
dbname = "music_library"
dbuser = os.environ["db_user"]
pwd = os.environ["db_pwd"]     # DO NOT hard-code this

# create SQL engine for DB
engine = sql.create_engine(f'mysql+mysqlconnector://{dbuser}:{pwd}@{host}:{port}/{dbname}')

# SET UP FLASK APPLICATION
app = Flask(__name__)


@app.route('/')
def index():
    # index route for webpage
    # if cookie does not exist, then the get function returns None
    user = request.cookies.get('userID')
    if user is not None:
        render_template("index.html", user=user)
    return render_template("index.html")


@app.route('/about')
def about():
    # return static information for about page
    # check if user is logged in to pass correct variables to template
    user = request.cookies.get('userID')
    if user is not None:
        render_template("about.html", user=user)
    return render_template("about.html")


@app.route('/contact')
def contact():
    # return static contact page, check if user
    # is logged in to pass correct variables to template
    user = request.cookies.get('userID')
    if user is not None:
        render_template("contact.html", user=user)
    return render_template("contact.html")


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        # verify that the passwords match
        # verify that the username and email are unused and
        # update the user information with the new data
        # tutorial on sql: https://chartio.com/resources/tutorials/how-to-execute-raw-sql-in-sqlalchemy/
        # https://stackoverflow.com/questions/20971680/sql-server-insert-if-not-exists
        pass
    # create page to allow users to sign up
    return render_template("signup.html")


@app.route('/login', methods=['POST', 'GET'])
def login():
    # login page for user
    if request.method == 'POST':
        # verify user exists and validate password is correct
        # create user authorization cookie
        if not request.cookies.get('foo'):
            res = make_response("Setting a cookie")
            res.set_cookie('foo', 'bar', max_age=60 * 60 * 24 * 365 * 2)
        return redirect(url_for('browse'))
    else:
        return render_template("login.html")


@app.route('/logout')
def logout():
    # delete user authorization cookie
    # redirect to index
    return redirect(url_for('index'))


@app.route('/browse')
def browse():
    # webpage to allow user to browse playlists
    # use the url parameters to define different access paths
    # parameter options: playlist = id, album = id, artist = id, view = {"recent", "top200", "new"}
    return 'Hello, World!'


@app.route('/sitemap')
def sitemap():
    # list all of the links to pages on the site
    return 'Hello, World!'


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app.run(use_reloader=True)

