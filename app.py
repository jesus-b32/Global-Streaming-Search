import os
import requests
import json

from flask import Flask, render_template, request, flash, redirect, session, g, url_for
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError

from forms import UserAddForm, LoginForm, UserEditForm
from models import db, connect_db, User, Region, Video, VideoList, Genre, GenreList, StreamingProvider, StreamingList

CURR_USER_KEY = "curr_user"
# BASE_URL = 

app = Flask(__name__)
# Get DB_URI from environ variable (useful for production/testing) or,
# if not set there, use development local db.
app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgresql:///global-streaming-search'))

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']
toolbar = DebugToolbarExtension(app)

connect_db(app)
# with app.app_context():
#     db.drop_all()
#     db.create_all()



##############################################################################
# User signup/login/logout


#@app.before_request is a decorator used to register a function that is run before each request.
# When a request is received, Flask first calls any functions registered with @app.before_request (if any exist), and then proceeds to process the request.
# This feature is useful for tasks that need to be performed before each request, such as setting up a database connection, checking user authentication, or setting a custom logging object.
@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    # g is a special object in Flask used as a "generic data bucket" to share information across multiple requests.
    #This makes it a convenient place to store data that needs to be accessible across multiple parts of the application, but not retained between requests.
    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None


def do_login(user):
    """Log in user. Store user ID in session"""

    session[CURR_USER_KEY] = user.id


def do_logout():
    """Logout user. Remove user id from session"""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]


@app.route('/signup', methods=["GET", "POST"])
def signup():
    """Handle user signup.

    Create new user and add to DB. Redirect to home page.
    If form not valid, present form.
    If the there already is a user with that username: flash message
    and re-present form.
    """

    form = UserAddForm()

    if form.validate_on_submit():
        try:
            user = User.signup(
                username=form.username.data,
                password=form.password.data,
                email=form.email.data,
                image_url=form.image_url.data or User.image_url.default.arg,
            )
            db.session.commit()

        except IntegrityError:
            flash("Username already taken", 'danger')
            return render_template('signup.html', form=form)

        do_login(user)

        return redirect("/")

    else:
        return render_template('signup.html', form=form)


@app.route('/login', methods=["GET", "POST"])
def login():
    """Handle user login."""

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data,
                                form.password.data)

        if user:
            do_login(user)
            flash(f"Hello, {user.username}!", "success")
            return redirect("/")

        flash("Invalid credentials.", 'danger')

    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    """Handle logout of user."""

    do_logout()
    flash("Successfully Logged Out!", "info")
    return redirect(url_for('login'))



##############################################################################
# Homepage and error pages


@app.route('/')
def homepage():
    """Show homepage:

    - anon users: no messages
    - logged in: 100 most recent messages of followed_users
    """

    if g.user:

        #list of users current user is following.
        #can access message id, username, emai, messages, etc..        
        

        return render_template('home.html')

    else:
        return render_template('home-anon.html')


##############################################################################



##############################################################################
# General user routes:

@app.route('/users')
def list_users():
    """Search page with listing of users.

    Can take a 'q' parameter in querystring to search by that username.
    """

    search = request.args.get('q')

    if not search:
        users = User.query.all()
    else:
        users = User.query.filter(User.username.like(f"%{search}%")).all()

    return render_template('users/index.html', users=users)


# @app.route('/users/<int:user_id>')
# def users_show(user_id):
#     """Show user profile."""

#     user = User.query.get_or_404(user_id)

#     # snagging messages in order from the database;
#     # user.messages won't be in order by default
#     messages = (Message
#                 .query
#                 .filter(Message.user_id == user_id)
#                 .order_by(Message.timestamp.desc())
#                 .limit(100)
#                 .all())
#     return render_template('users/show.html', user=user, messages=messages)


##############################################################################
# TMDB routes:

@app.route('/search/movie')
def movie_search():
    """Search page with listing of movies, TV shows, and people.

    Can take a 'q' parameter in querystring to search by that username.
    """

    search = request.args.get('search')
    movie_url = f"https://api.themoviedb.org/3/search/movie?query={search}&include_adult=false&language=en-US&page=1"

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJiYmNiNDk2NzgyY2E1MTdlZDVjZmQ0MDhmM2YxZWRiZCIsInN1YiI6IjY2MmViMjY4MjRmMmNlMDEyMzJhZDJjZCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ._z0ha6kQXHFrcvQVPzH0xbYLXSVs1pVwvbqgxVfdyiI"
    }
    # movies request
    movie_response = requests.get(movie_url, headers=headers)
    movie_data = movie_response.json()
    # print(movie_response.json())
    # movie_result = movie_responseresults
    # movie_page = movie_response.page
    # movie_total_pages = movie_response.total_pages
    # movie_total_results = movie_response.total_results
    
        
    return render_template('movie_results.html',
                            search=search,
                            movie_data=movie_data)

    
@app.route('/search/tv')
def tv_search():
    """Search page with listing of movies, TV shows, and people.

    Can take a 'q' parameter in querystring to search by that username.
    """

    search = request.args.get('q')
    tv_url = f"https://api.themoviedb.org/3/search/tv?query={search}&include_adult=false&language=en-US&page=1"

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJiYmNiNDk2NzgyY2E1MTdlZDVjZmQ0MDhmM2YxZWRiZCIsInN1YiI6IjY2MmViMjY4MjRmMmNlMDEyMzJhZDJjZCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ._z0ha6kQXHFrcvQVPzH0xbYLXSVs1pVwvbqgxVfdyiI"
    }
    
    # tv shows request
    tv_response = requests.get(tv_url, headers=headers)
    # tv_result = tv_response.results
    # tv_page = tv_response.page
    # tv_total_pages = tv_response.total_pages
    # tv_total_results = tv_response.total_results
    # print(response.text)

    # if not search:
    #     # users = User.query.all()
    # else:
    #     # users = User.query.filter(User.username.like(f"%{search}%")).all()
        
    return render_template('search_results.html',
                            search=search,
                            tv_response=tv_response)