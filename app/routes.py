from flask import render_template, flash, redirect, url_for, request
from app import app
from app.forms import LoginForm, UserRegisterForm
from flask_login import current_user, login_user, logout_user
import sqlalchemy as sa
from app import db
from app.models import User, Region, VideoList, VideoListVideos
from app.forms import UserRegisterForm, LoginForm

from urllib.parse import urlsplit
import app.api as api




@app.route('/signup', methods=["GET", "POST"])
def signup():
    """Handle user signup.

    Create new user and add to DB. Redirect to home page.
    If form not valid, present form.
    If the there already is a user with that username: flash message
    and re-present form.
    """
    if current_user.is_authenticated:
        return redirect(url_for('homepage'))
    
    form = UserRegisterForm()

    if form.validate_on_submit():
        user = User(username = form.username.data,
                    profile_image=form.profile_image)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulation, you are now a register user!')
        
        return redirect(url_for('login'))
    
    return render_template('signup.html', form=form)


@app.route('/login', methods=["GET", "POST"])
def login():
    """Handle user login."""
    
    if current_user.is_authenticated:
        return redirect(url_for('homepage'))

    form = LoginForm()
    if form.validate_on_submit():
        # user = User.authenticate(form.username.data,
        #                         form.password.data)
        user = db.session.scalar(sa.select(User).where(User.username == form.username.data))

        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('homepage')
        
        return redirect(url_for('homepage'))
    
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    """Handle logout of user."""
    
    logout_user()
    return redirect(url_for('homepage'))



##############################################################################
# Homepage and error pages


@app.route('/')
def homepage():
    """Show homepage:

    - anon users: no messages
    - logged in: 100 most recent messages of followed_users
    """

    # if current_user:

    #     #list of users current user is following.
    #     #can access message id, username, emai, messages, etc..        
        

    #     return render_template('home.html')

    # else:
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
    countries = api.country_list()
    
    #gets the name of the country user selected
    country = db.get_or_404(Region, country_selected)
    # all_countries = db.
    
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
                            country=country)

    
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
    countries = api.country_list()
    
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