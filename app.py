import os

from flask import Flask, render_template, request, flash, redirect, session, g, url_for
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError

from forms import UserAddForm, LoginForm, UserEditForm
from models import db, connect_db, User, Region, Video, VideoList, Genre, GenreList, StreamingProvider, StreamingList

import api

CURR_USER_KEY = "curr_user"

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
    
    
@app.route('/about')
def about():
    """Show about section:

    - anon users: no messages
    - logged in: 100 most recent messages of followed_users
    """

    return render_template('about.html')


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
# Movie routes:

@app.route('/search/movie')
def movie_searching():
    """Search page with listing of movies, TV shows, and people.

    Can take a 'q' parameter in querystring to search by that username.
    """

    search = request.args.get('search')
    movie_data = api.movie_search(search)
        
    return render_template('movie_results.html',
                            search=search,
                            movie_data=movie_data)


def get_provider_name(id, provider_data):
    for provider in provider_data['results']:
        if provider['provider_id'] == id:
            return provider['provider_name']
        

def get_country_name(id, country_data):
    for country in country_data['results']:
        if country['iso_3166_1'] == id:
            return country['native_name']
    

    
@app.route('/movie/<int:movie_id>')
def movie_detail(movie_id):
    """Movie detail page that lists important movie details. ALso displays streaming availability by country or by streaming provider, based on what user selects.
    Can take a 'country' parameter in querystring to search by that username.
    """
    #user selected country for sreaming info
    country_selected = request.args.get('country')
    if not country_selected: #default to US if no country picked
        country_selected = 'US'
    
    provider_selected = request.args.get('streamingProvider', type=int)
    #default to netflix if no provider picked
    if not provider_selected:
        provider_selected = 8
    
    #list of countries with streaming data
    countries = api.get_country_list()
    
    #gets the name of the country user selected
    country_name = get_country_name(country_selected, countries)
    
    #list of streamingn providers for movies
    providers = api.movie_provider_list()
    
    #gets the name of the provider user selected
    provider_name = get_provider_name(provider_selected, providers)
    
    # movie detail including streaming provider info
    movie_data = api.movie_details(movie_id)
    
    return render_template('movie_detail.html',
                            movie_data=movie_data,
                            providers=providers,
                            countries=countries,
                            country_selected=country_selected,
                            provider_selected=provider_selected,
                            provider_name=provider_name,
                            country_name=country_name)

    
@app.route('/search/tv')
def tv_searching():
    """Search page with listing of movies, TV shows, and people.

    Can take a 'q' parameter in querystring to search by that username.
    """

    search = request.args.get('search')
    tv_data = api.tv_search(search)
        
    return render_template('tv_results.html',
                            search=search,
                            tv_data=tv_data)
    
    
    
@app.route('/tv/<int:tv_id>')
def tv_detail(tv_id):
    """TV detail page that lists important tv show details. ALso displays streaming availability by country or by streaming provider, based on what user selects.
    Can take a 'country' parameter in querystring to search by that username.
    """
    #user selected country for sreaming info
    country_selected = request.args.get('country')
    if not country_selected: #default to US if no country picked
        country_selected = 'US'
    
    provider_selected = request.args.get('streamingProvider', type=int)
    #default to netflix if no provider picked
    if not provider_selected:
        provider_selected = 8
    
    #list of countries with streaming data
    countries = api.get_country_list()
    
    #gets the name of the country user selected
    country_name = get_country_name(country_selected, countries)
    
    #list of streamingn providers for movies
    providers = api.tv_provider_list()
    
    #gets the name of the provider user selected
    provider_name = get_provider_name(provider_selected, providers)
    
    # tv show detail including streaming provider info
    tv_data = api.tv_details(tv_id)
    
    return render_template('tv_detail.html',
                            tv_data=tv_data,
                            providers=providers,
                            countries=countries,
                            country_selected=country_selected,
                            provider_selected=provider_selected,
                            provider_name=provider_name,
                            country_name=country_name)