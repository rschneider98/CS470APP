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
import numpy as np
import pandas as pd       # used to execute SQL statements on sqlalchemy engine
import hashlib            # cryptographic hash for user verification
from secrets import token_bytes

# SET ENVIRONMENT VARIABLES FOR DB
# since this will be run at the same location as DB these are formatted for local connections to DB
#host = "127.0.0.1"  # localhost
host = "raspberrypi"
port = 3306         # local port
dbname = "music_library"
dbuser = os.environ["db_user"]
pwd = os.environ["db_pwd"]     # DO NOT hard-code this

# create SQL engine for DB
engine = sql.create_engine(f'mysql+mysqlconnector://{dbuser}:{pwd}@{host}:{port}/{dbname}')

# SET UP FLASK APPLICATION
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ['FLASK_KEY']


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
        first_name = request.form["first_name"].strip()
        last_name = request.form["last_name"].strip()
        username = request.form["username"].strip()
        password = request.form["password"].strip()
        confirm_password = request.form["confirm_password"].strip()
        # verify that the passwords match
        if password != confirm_password:
            flash("Passwords must match")
            return render_template("signup.html")
        # verify that the username and email are unused and
        # update the user information with the new data
        salt = token_bytes(8)
        hashed_pwd = hashlib.sha3_256(b''.join([salt, bytes(password, 'utf=8')])).digest()
        with open('sql/add_user.sql', mode='r') as f:
            f_text = f.read()
        query = text(f_text)
        try:
            with engine.connect() as connection:
                connection.execute(query,
                                   user_name=username,
                                   user_password=hashed_pwd,
                                   salt=salt,
                                   email=email,
                                   first=first_name,
                                   last=last_name)
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
        with open('sql/validate_user.sql', mode='r') as f:
            f_text = f.read()
        query = text(f_text)
        with engine.connect() as connection:
            result = connection.execute(
                query,
                user=submitted_user
            )
            # process result into keys and values (fetchall should not be a problem here)
            keys = result.keys()
            values = result.fetchall()
            # verify that result has one row
            # there is a constraint in the database that this should be unique
            if len(values) == 0:
                flash("Username and Password do not match")
                return render_template("login.html")
            # compute the hash of password
            user_info = dict(zip(keys, np.array(values).transpose().tolist()))
            salt = user_info["salt"][0]
            validation_pwd = user_info["userPassword"][0]
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
    # webpage to allow user to browse search results
    user = session.get('user')
    if user is not None:
        # show user's playlists
        # get the information requested

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
    user = session.get('user')
    if user is not None:
        # get the information requested
        # the songs in the playlist in order of: index, song name, artist name, album, artist id, album id
        with open('sql/get_playlist_songs.sql', mode='r') as f:
            f_text = f.read()
        query = text(f_text)
        with engine.connect() as connection:
            result = connection.execute(
                query,
                playlist_id=playlist
            )
            # process result into keys and values (fetchall should not be a problem here)
            keys = result.keys()
            values = result.fetchall()

        rows = [[i + 1] + list(values[i]) for i in range(len(values))]

        with open('sql/get_playlist_name.sql', mode='r') as f:
            f_text = f.read()
        query = text(f_text)
        with engine.connect() as connection:
            result = connection.execute(
                query,
                playlist_id=playlist
            )
            # process result into keys and values (fetchall should not be a problem here)
            keys = result.keys()
            values = result.fetchall()
            playlists = values
            name = values[0][0]

        # call separate sql with sqlalchemy to get name of playlist, user name, etc.
        return render_template("browse.html", user=user, rows=rows, playlists=playlists, title=name)
    return redirect(url_for('login'))


@app.route('/browse/<int:artist>/<int:album>')
def browse_album(artist, album):
    # webpage to allow user to browse albums
    # use the url parameters to define different access paths
    user = session.get('user')
    if user is not None:
        with open('sql/get_album.sql', mode='r') as f:
            f_text = f.read()
        query = text(f_text)
        with engine.connect() as connection:
            result = connection.execute(
                query,
                artist_id=artist,
                album_id=album
            )
            # process result into keys and values (fetchall should not be a problem here)
            keys = result.keys()
            values = result.fetchall()

        rows = [[i + 1] + list(values[i]) for i in range(len(values))]

        with open('sql/get_album_name.sql', mode='r') as f:
            f_text = f.read()
        query = text(f_text)
        with engine.connect() as connection:
            result = connection.execute(
                query,
                artist_id=artist,
                album_id=album
            )
            # process result into keys and values (fetchall should not be a problem here)
            keys = result.keys()
            values = result.fetchall()
            playlists = values
            name = values[0][0]

        # call separate sql with sqlalchemy to get name of playlist, user name, etc.
        return render_template("browse.html", user=user, rows=rows, playlists=playlists, title=name)
    return redirect(url_for('login'))


@app.route('/browse/<int:artist>')
def browse_artist(artist):
    # webpage to allow user to browse playlists
    # use the url parameters to define different access paths
    user = session.get('user')
    if user is not None:
        # get the information requested
        # columns will be index, album name, year of release, artist id, album id
        with open('sql/get_artist.sql', mode='r') as f:
            f_text = f.read()
        query = text(f_text)
        with engine.connect() as connection:
            result = connection.execute(
                query,
                artist_id=artist
            )
            # process result into keys and values (fetchall should not be a problem here)
            keys = result.keys()
            values = result.fetchall()

        rows = [[i + 1] + list(values[i]) for i in range(len(values))]

        with open('sql/get_artist_name.sql', mode='r') as f:
            f_text = f.read()
        query = text(f_text)
        with engine.connect() as connection:
            result = connection.execute(
                query,
                artist_id=artist
            )
            # process result into keys and values (fetchall should not be a problem here)
            keys = result.keys()
            values = result.fetchall()
            playlists = values
            name = values[0][0]

        return render_template("browse_albums.html", user=user, rows=rows, playlists=playlists, title=name)
    return redirect(url_for('login'))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app.run(use_reloader=True)

