# This is the main app script for flask that will handles requests to the webpage

import os                 # used to get environment variables so we don't store passwords
# python web-framework
from flask import (
    Flask,
    redirect,
    url_for,
    request,
    render_template
)
import mysql              # mysql connector library
import sqlalchemy as sql  # sqlalchemy is used to connect to db
import pandas as pd       # used to execute SQL statements on sqlalchemy engine
import sha3               # cryptographic hash for user verification

# SET ENVIRONMENT VARIABLES FOR DB
# since this will be run at the same location as DB these are formatted for local connections to DB
host = "127.0.0.1"  # localhost
port = 3306         # local port
dbname = "music_library"
user = os.environ["db_user"]
pwd = os.environ["db_pwd"]     # DO NOT hard-code this

# create SQL engine for DB
engine = sql.create_engine(f'mysql+mysqlconnector://{user}:{pwd}@{host}:{port}/{dbname}')

# SET UP FLASK APPLICATION
app = Flask(__name__)


@app.route('/')
def index():
    # index route for webpage
    return render_template("index.html")


@app.route('/about')
def about():
    # return static information for about page
    return 'Hello, World!'


@app.route('/contact')
def contact():
    # return static contact page
    return 'Hello, World!'


@app.route('/signup')
def signup():
    # create page to allow users to sign up
    return 'Hello, World!'


@app.route('/login', methods=['POST', 'GET'])
def login():
    # login page for user
    if request.method == 'POST':
        # verify user exists and validate password is correct
        # create user authorization cookie
        user = request.form['nm']
        return redirect(url_for('browse'))
    else:
        return render_template("login.html")


@app.route('/logout')
def logout():
    # delete user authorization cookie
    # redirect to index
    return 'Hello, World!'


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





def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
