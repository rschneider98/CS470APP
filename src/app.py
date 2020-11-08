# This is the main app script for flask that will handles requests to the webpage

import os                 # used to get environment variables so we don't store passwords
# python web-framework
from flask import (
    Flask,
    redirect,
    flash,
    url_for,
    request,
    session,
    make_response,
    render_template
)
import mysql              # mysql connector library
# sqlalchemy is used to connect to db
import sqlalchemy as sql
from sqlalchemy.sql import text
from sqlalchemy.exc import IntegrityError
from sqlalchemy import (
    Table,
    Column,
    Integer,
    LargeBinary,
    String,
    MetaData
)
import pandas as pd       # used to execute SQL statements on sqlalchemy engine
import hashlib            # cryptographic hash for user verification
import random

# SET ENVIRONMENT VARIABLES FOR DB
# since this will be run at the same location as DB these are formatted for local connections to DB
#host = "127.0.0.1"  # localhost
host = "raspberrypi"
port = 3306         # local port
dbname = "music_library"
dbuser = os.environ["db_user"]
pwd = os.environ["db_pwd"]     # DO NOT hard-code this

# create SQL engine for DB
#engine = sql.create_engine(f'mysql+mysqlconnector://{dbuser}:{pwd}@{host}:{port}/{dbname}')

# make formats for SQL queries that will be processed by SQLalchemy
# sqlalchemy will filter inputs to delimit special characters
SQL_VERIFY_USER = text("SELECT user.salt, user.pwd FROM user WHERE user.username = :user")

# tables for sqlalchemy
#meta = MetaData(engine).reflect()
#user_table = meta.tables['user']

'''user_table = Table(
   'user', meta,
   Column('email', String(255), primary_key=True),
   Column('username', String(15), primary_key=True),
   Column('salt', LargeBinary(20)),
   Column('pwd', LargeBinary(512)),
)'''

# SET UP FLASK APPLICATION
app = Flask(__name__)
app.config['SECRET_KEY'] = 'super secret'


@app.route('/')
def index():
    # index route for webpage
    # if cookie does not exist, then the get function returns None
    user = session.get('user')
    if user is not None:
        render_template("index.html", user=user)
    return render_template("index.html")


@app.route('/about')
def about():
    # return static information for about page
    # check if user is logged in to pass correct variables to template
    user = session.get('user')
    if user is not None:
        render_template("about.html", user=user)
    return render_template("about.html")


@app.route('/contact')
def contact():
    # return static contact page, check if user
    # is logged in to pass correct variables to template
    user = session.get('user')
    if user is not None:
        render_template("contact.html", user=user)
    return render_template("contact.html")


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        email = request.form["email"].strip()
        username = request.form["username"].strip()
        password = request.form["password"].strip()
        confirm_password = request.form["confirm_password"].strip()
        # verify that the passwords match
        if password != confirm_password:
            flash("Passwords must match")
            return render_template("signup.html")
        # verify that the username and email are unused and
        # update the user information with the new data
        salt = random.randbytes(20)
        hashed_pwd = hashlib.sha_512(b''.join([salt, password])).digest()
        try:
            with engine.connect() as connection:
                add_user = user_table.insert().values(email=email, user=username, salt=salt, pwd=hashed_pwd)
                connection.execute(add_user)
        except IntegrityError:
            flash("Username or Email already taken")
            return render_template("signup.html")
        session['user'] = username
        return redirect(url_for('browse'))
    # create page to allow users to sign up
    return render_template("signup.html")


@app.route('/login', methods=['POST', 'GET'])
def login():
    # login page for user
    if request.method == 'POST':
        # verify user exists and validate password is correct
        submitted_user = request.form["username"].strip()
        submitted_pwd = request.form["password"].strip()

        # REMOVE: for testing purpose only
        if submitted_user == "admin" and submitted_pwd == "admin":
            session['user'] = submitted_user
            return redirect(url_for('browse'))

        # SQL request to get salt and hash of the user
        with engine.connect() as connection:
            result = connection.execute(
                SQL_VERIFY_USER,
                user=submitted_user
            )
            # verify that result has one row
            # there is a constraint in the database that this should be unique
            if result.count() == 0:
                flash("Username and Password do not match")
                return render_template("login.html")
            # compute the hash of password
            user_info = result.first()
            salt = result["salt"]
            validation_pwd = result["pwd"]
            hashed_pwd = hashlib.sha3_512(b"".join([salt, submitted_pwd])).digest()
            # create user authorization cookie
            if validation_pwd == hashed_pwd:
                session['user'] = submitted_user
            else:
                flash("Username and Password do not match")
                return render_template("login.html")
        return redirect(url_for('browse'))
    else:
        return render_template("login.html")


@app.route('/logout')
def logout():
    # delete user authorization cookie
    session.pop('user', None)
    # redirect to index
    return redirect(url_for('index'))


@app.route('/browse')
def browse():
    # webpage to allow user to browse playlists
    # use the url parameters to define different access paths
    # parameter options: playlist = id, album = id, artist = id, view = {"recent", "top200", "new"}
    user = session.get('user')
    if user is not None:
        # show liked songs
        # get the information requested
        df = None
        title = "folklore"
        subtitle = "Taylor Swift"
        rows = [
            ("1", "the 1", "Taylor Swift", "folklore", "1", "7", "LINK"),
            ("2", "cardigan", "Taylor Swift", "folklore", "1", "7", "LINK"),
            ("3", "the last great american dynasty", "Taylor Swift", "folklore", "1", "7", "LINK"),
            ("4", "exile (feat. Bon Iver)", "Taylor Swift", "folklore", "1", "7", "LINK"),
            ("5", "my tears ricochet", "Taylor Swift", "folklore", "1", "7", "LINK"),
            ("6", "mirrorball", "Taylor Swift", "folklore", "1", "7", "LINK"),
            ("7", "seven", "Taylor Swift", "folklore", "1", "7", "LINK"),
            ("8", "august", "Taylor Swift", "folklore", "1", "7", "LINK"),
            ("9", "this is me trying", "Taylor Swift", "folklore", "1", "7", "LINK"),
            ("10", "illicit affairs", "Taylor Swift", "folklore", "1", "7", "LINK"),
            ("11", "invisible string", "Taylor Swift", "folklore", "1", "7", "LINK"),
            ("12", "mad woman", "Taylor Swift", "folklore", "1", "7", "LINK"),
            ("13", "epiphany", "Taylor Swift", "folklore", "1", "7", "LINK"),
            ("14", "betty", "Taylor Swift", "folklore", "1", "7", "LINK"),
            ("15", "peace", "Taylor Swift", "folklore", "1", "7", "LINK"),
            ("16", "hoax", "Taylor Swift", "folklore", "1", "7", "LINK"),
        ]
        return render_template("browse.html", user=user, rows=rows, title=title, subtitle=subtitle)
    return redirect(url_for('login'))


@app.route('/playlist/<int:playlist>')
def browse_playlist(playlist):
    # webpage to allow user to browse playlists
    # use the url parameters to define different access paths
    # parameter options: playlist = id, album = id, artist = id, view = {"recent", "top200", "new"}
    user = session.get('user')
    if user is not None:
        # get the information requested
        df = None
        colnames = list(df.columns)
        rows = list(df.to_records(index=False))
        # call separate sql with sqlalchemy to get name of playlist, user name, etc.
        return render_template("browse.html", user=user, columns=colnames, rows=rows, title=name)
    return redirect(url_for('login'))


@app.route('/browse/<int:artist>/<int:album>')
def browse_album(artist, album):
    # webpage to allow user to browse playlists
    # use the url parameters to define different access paths
    # parameter options: playlist = id, album = id, artist = id, view = {"recent", "top200", "new"}
    user = session.get('user')
    if user is not None:
        # get the information requested
        df = None
        title = "folklore"
        subtitle = "Taylor Swift"
        rows = [
            ("1", "the 1", "Taylor Swift", "folklore", "1", "7", "LINK"),
            ("2", "cardigan", "Taylor Swift", "folklore", "1", "7", "LINK"),
            ("3", "the last great american dynasty", "Taylor Swift", "folklore", "1", "7", "LINK"),
            ("4", "exile (feat. Bon Iver)", "Taylor Swift", "folklore", "1", "7", "LINK"),
            ("5", "my tears ricochet", "Taylor Swift", "folklore", "1", "7", "LINK"),
            ("6", "mirrorball", "Taylor Swift", "folklore", "1", "7", "LINK"),
            ("7", "seven", "Taylor Swift", "folklore", "1", "7", "LINK"),
            ("8", "august", "Taylor Swift", "folklore", "1", "7", "LINK"),
            ("9", "this is me trying", "Taylor Swift", "folklore", "1", "7", "LINK"),
            ("10", "illicit affairs", "Taylor Swift", "folklore", "1", "7", "LINK"),
            ("11", "invisible string", "Taylor Swift", "folklore", "1", "7", "LINK"),
            ("12", "mad woman", "Taylor Swift", "folklore", "1", "7", "LINK"),
            ("13", "epiphany", "Taylor Swift", "folklore", "1", "7", "LINK"),
            ("14", "betty", "Taylor Swift", "folklore", "1", "7", "LINK"),
            ("15", "peace", "Taylor Swift", "folklore", "1", "7", "LINK"),
            ("16", "hoax", "Taylor Swift", "folklore", "1", "7", "LINK"),
        ]
        return render_template("browse.html", user=user, rows=rows, title=title, subtitle=subtitle)
    return redirect(url_for('login'))


@app.route('/browse/<int:artist>')
def browse_artist(artist):
    # webpage to allow user to browse playlists
    # use the url parameters to define different access paths
    # parameter options: playlist = id, album = id, artist = id, view = {"recent", "top200", "new"}
    user = session.get('user')
    if user is not None:
        # get the information requested
        df = None
        title = "Taylor Swift"
        rows = [
            ("1", "Taylor Swift", "2006", "1", "1", "LINK"),
            ("2", "Fearless", "2008", "1", "2", "LINK"),
            ("3", "Speak Now", "2010", "1", "3", "LINK"),
            ("4", "Red", "2012", "1", "4", "LINK"),
            ("5", "1989", "2014", "1", "5", "LINK"),
            ("6", "reputation", "2017", "1", "6", "LINK"),
            ("7", "Lover", "2019", "1", "7", "LINK"),
            ("8", "folklore", "2020", "1", "8", "LINK")
        ]
        return render_template("browse_albums.html", user=user, rows=rows, title=title)
    return redirect(url_for('login'))


@app.route('/browse/<view>')
def browse_view(view):
    # webpage to allow user to browse playlists
    # use the url parameters to define different access paths
    # parameter options: playlist = id, album = id, artist = id, view = {"recent", "top200", "new"}
    user = session.get('user')
    if user is not None:
        # get the information requested
        df = None

        return render_template("browse.html", user=user, columns=colnames, rows=rows, title=name)
    return redirect(url_for('login'))


@app.route('/sitemap')
def sitemap():
    # list all of the links to pages on the site
    return 'Hello, World!'


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app.run(use_reloader=True)

