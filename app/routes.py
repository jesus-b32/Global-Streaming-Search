from flask import render_template, flash, redirect, url_for, request
from app import app, db
from flask_login import current_user, login_user, logout_user
import sqlalchemy as sa
from app.models import User, Country, VideoList, VideoListVideos
from app.forms import UserRegisterForm, LoginForm

from urllib.parse import urlsplit
import app.api as api


@app.template_global('get_country_name')        
def get_country_name(id):
    """Take country ID and retrieve the country name in Region table from database. The @app.template_global decerator creates a global function that can be used in any jinja template.

    Args:
        id (string): id of country in Region table in database

    Returns:
        string: The country name associated with the country id enter
    """
    
    country = db.session.get(Country, id)
    # if country not found in database, return country ID
    if not country:
        return id
    return country.name     


# @app.template_global('video_detail')        
# def get_country_name(tmdb_id, media_type):
#     """Take country ID and retrieve the country name in Region table from database. The @app.template_global decerator creates a global function that can be used in any jinja template.

#     Args:
#         id (string): id of country in Region table in database

#     Returns:
#         string: The country name associated with the country id enter
#     """
    
#     country = db.session.get(Country, id)
#     # if country not found in database, return country ID
#     if not country:
#         return id
#     return country.name    




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
                    profile_image=form.profile_image.data or User.profile_image.default.arg)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        
        #giver new user a watchlist and favorites list
        watchlist = VideoList(user_id = user.id,
                            name = 'watchlist')
        favorites = VideoList(user_id = user.id,
                            name = 'favorites')
        db.session.add_all([watchlist, favorites])
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
        user = db.session.scalar(sa.select(User).where(User.username == form.username.data))

        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        
        # login user. Handle the case where user attempted to access a login restricted page. After user successfully logs in, user should be redirected to the page user wanted to access.
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        
        # if login URL has not next argument or URL is set to a full URL that includes a domain name, then redirect to homepage
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('homepage')

        return redirect(next_page)
    
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

    return render_template('home-anon.html')
    
    
@app.route('/about')
def about():
    """Show about section.

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


@app.route('/search')
def search():
    """Redirect to movie or tv show result page based on user selection

    """

    search = request.args.get('search')
    media_type = request.args.get('media_type')
        
    if media_type == 'movie':
        return redirect(url_for('movie_searching', search=search))
    
    return redirect(url_for('tv_searching', search=search))


##############################################################################
# Movie routes:

@app.route('/search/movie')
def movie_searching():
    """Search result page with listing of movies that query search term

    """

    search = request.args.get('search')
    movie_data = api.movie_search(search)
        
    return render_template('movie_results.html',
                            search=search,
                            movie_data=movie_data)

    
@app.route('/movie/<int:movie_id>')
def movie_detail(movie_id):
    """Movie detail page that lists important movie details. ALso displays streaming availability by country or by streaming provider, based on what user selects.
    Can take a 'country' or provider parameter in querystring to search for streaming availabliltiy by that term.
    """
    #user selected country for sreaming info
    country_selected = request.args.get('country')
    if not country_selected: #default to US if no country picked
        country_selected = 'US'
    
    #user selected provider for sreaming info
    provider_selected = request.args.get('streamingProvider', type=int)
    #default to netflix if no provider picked
    if not provider_selected:
        provider_selected = 8
    
    #list of countries with streaming data
    countries = api.country_list()
    
    #list of streamingn providers for movies
    providers = api.movie_provider_list()
    
    #gets the name of the provider user selected
    provider_name = api.get_provider_name(provider_selected, providers)
    
    # movie detail including streaming provider info
    movie_data = api.movie_details(movie_id)
    
    return render_template('movie_detail.html',
                            movie_data=movie_data,
                            providers=providers,
                            countries=countries,
                            country_selected=country_selected,
                            provider_selected=provider_selected,
                            provider_name=provider_name)
#############################################################################

############################################################################
#TV routes
    
@app.route('/search/tv')
def tv_searching():
    """Search result page with listing of movies that query search term

    """

    search = request.args.get('search')
    tv_data = api.tv_search(search)
        
    return render_template('tv_results.html',
                            search=search,
                            tv_data=tv_data)


@app.route('/tv/<int:tv_id>')
def tv_detail(tv_id):
    """TV detail page that lists important tv show details. ALso displays streaming availability by country or by streaming provider, based on what user selects.
    Can take a 'country' or provider parameter in querystring to search for streaming availabliltiy by that term.
    """
    #user selected country for sreaming info
    country_selected = request.args.get('country')
    if not country_selected: #default to US if no country picked
        country_selected = 'US'
    
    #user selected provider for sreaming info
    provider_selected = request.args.get('streamingProvider', type=int)
    #default to netflix if no provider picked
    if not provider_selected:
        provider_selected = 8
    
    #list of countries with streaming data
    countries = api.country_list()
    
    #list of streamingn providers for tv shows
    providers = api.tv_provider_list()
    
    #gets the name of the provider user selected
    provider_name = api.get_provider_name(provider_selected, providers)
    
    # tv show detail including streaming provider info
    tv_data = api.tv_details(tv_id)
    
    return render_template('tv_detail.html',
                            tv_data=tv_data,
                            providers=providers,
                            countries=countries,
                            country_selected=country_selected,
                            provider_selected=provider_selected,
                            provider_name=provider_name)
#############################################################################

#############################################################################
# video lists routes    
    
@app.route('/user/<int:user_id>/watchlist')
def watchlist(user_id):
    """Search result page with listing of movies that query search term

    """
    # user = db.session.get(User, user_id)
    watchlist = db.session.scalar(sa.select(VideoList).where(VideoList.user_id == user_id, VideoList.name == 'watchlist'))
    
    # for video in video_list.videos:
        
        
    return render_template('watchlist.html', watchlist)    