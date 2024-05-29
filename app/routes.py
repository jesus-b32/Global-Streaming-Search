from flask import render_template, flash, redirect, url_for, request
from app import app, db
from flask_login import current_user, login_user, logout_user, login_required
import sqlalchemy as sa
from app.models import User, Country, VideoList, Video
from app.forms import UserRegisterForm, LoginForm, EditProfileForm

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



##############################################################################
# User signup/login/logout

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
        
        #give new user a watchlist
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

        # flash message if no user found or invalid password
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

    """

    return render_template('home.html')
    
    
@app.route('/about')
def about():
    """Show about section.

    """

    return render_template('about.html')


##############################################################################



##############################################################################
# General user routes:

@app.route('/edit_profile', methods=["GET", "POST"])
@login_required
def edit_profile():
    """Show user profile and allow to edit username and profile image."""

    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.profile_image = form.profile_image.data
        db.session.commit()
        flash('Your changes have been saved')
        return redirect(url_for('edit_profile'))
    # prefill form with user data
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.profile_image.data = current_user.profile_image
    return render_template('edit_profile.html', form=form)


@app.route('/search')
def search():
    """Redirect to movie or tv show result page based on user selection

    """

    search = request.args.get('search')
    media_type = request.args.get('media_type')
        
    if media_type == 'movie':
        return redirect(url_for('movie_searching', search=search, page=1))
    
    return redirect(url_for('tv_searching', search=search, page=1))


##############################################################################
# Movie routes:

@app.route('/search/movie/')
def movie_searching():
    """Search result page with listing of movies from query search term

    """

    search = request.args.get('search')
    current_page = request.args.get('page', type=int)
    movie_data = api.movie_search(search, current_page)
    
        
    return render_template('movie_results.html',
                            search=search,
                            movie_data=movie_data,
                            current_page=current_page)

    
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
    
    #json of countries with streaming data
    countries = api.country_list()
    
    #json of streamingn providers for movies
    providers = api.movie_provider_list()
    
    #gets the name of the provider user selected
    provider_name = api.get_provider_name(provider_selected, providers)
    
    # movie detail including streaming provider info
    movie_data = api.movie_details(movie_id)
    
    #check if this TV show is in user's watchlist
    if(current_user.is_authenticated):
        watchlist = db.session.scalar(sa.select(VideoList).where(VideoList.user_id == current_user.id, VideoList.name == 'watchlist'))
        
        in_watchlist = watchlist.video_is_in(movie_id, 'movie')
    else:
        in_watchlist = None
    
    
    return render_template('movie_detail.html',
                            movie_data=movie_data,
                            providers=providers,
                            countries=countries,
                            country_selected=country_selected,
                            provider_selected=provider_selected,
                            provider_name=provider_name,
                            in_watchlist=in_watchlist)
#############################################################################

############################################################################
#TV routes
    
@app.route('/search/tv/')
def tv_searching():
    """Search result page with listing of movies for that query search term

    """

    search = request.args.get('search')
    current_page = request.args.get('page', type=int)
    tv_data = api.tv_search(search, current_page)
        
    return render_template('tv_results.html',
                            search=search,
                            tv_data=tv_data,
                            current_page=current_page)


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
    
    #json of countries with streaming data
    countries = api.country_list()
    
    #json of streamingn providers for tv shows
    providers = api.tv_provider_list()
    
    #gets the name of the provider user selected
    provider_name = api.get_provider_name(provider_selected, providers)
    
    # tv show detail including streaming provider info
    tv_data = api.tv_details(tv_id)
    
    #check if this TV show is in user's watchlist
    if(current_user.is_authenticated):
        watchlist = db.session.scalar(sa.select(VideoList).where(VideoList.user_id == current_user.id, VideoList.name == 'watchlist'))
        
        in_watchlist = watchlist.video_is_in(tv_id, 'tv')
    else:
        in_watchlist = None
    
    
    return render_template('tv_detail.html',
                            tv_data=tv_data,
                            providers=providers,
                            countries=countries,
                            country_selected=country_selected,
                            provider_selected=provider_selected,
                            provider_name=provider_name,
                            in_watchlist=in_watchlist)
#############################################################################

#############################################################################
# video lists routes    
    
@app.route('/user/<int:user_id>/watchlist')
@login_required
def watchlist(user_id):
    """Display user watchlist

    """
    watchlist = db.session.scalar(sa.select(VideoList).where(VideoList.user_id == user_id, VideoList.name == 'watchlist'))
    
    query = watchlist.videos.select()
    videos = db.session.scalars(query).all() # make into a list
    
    video_list = [] # will contain the video and video detail grouped in dict
    
    for video in videos:
        video_detail = api.get_video_detail(video.tmdb_id, video.media_type)
        video_list.append({'video': video, 'video_detail': video_detail})    
        
        
    return render_template('watchlist.html', video_list=video_list)   



@app.route('/add/watchlist/<media_type>/<int:tmdb_id>', methods=['POST'])
@login_required
def add_to_watchlist(media_type, tmdb_id):
    """Add a movie or TV show to user watchlist

    """
    watchlist = db.session.scalar(sa.select(VideoList).where(VideoList.user_id == current_user.id, VideoList.name == 'watchlist'))
    video = db.session.scalar(sa.select(Video).where(Video.tmdb_id == tmdb_id, Video.media_type == media_type))
    
    if video is None:
        video = Video(tmdb_id=tmdb_id, media_type=media_type)
        db.session.add(video)
        watchlist.add_video(video)
        db.session.commit() 
    else:
        watchlist.add_video(video)
        db.session.commit()       
        
    if media_type == 'movie':
            return redirect(url_for('movie_detail', movie_id=tmdb_id))
    return redirect(url_for('tv_detail', tv_id=tmdb_id))


@app.route('/remove/watchlist/<media_type>/<int:tmdb_id>', methods=['POST'])
@login_required
def remove_from_watchlist(media_type, tmdb_id):
    """Remove a movie or TV show to user watchlist

    """
    watchlist = db.session.scalar(sa.select(VideoList).where(VideoList.user_id == current_user.id, VideoList.name == 'watchlist'))
    video = db.session.scalar(sa.select(Video).where(Video.tmdb_id == tmdb_id, Video.media_type == media_type))
    
    watchlist.remove_video(video)
    db.session.commit()    
        
    if media_type == 'movie':
            return redirect(url_for('movie_detail', movie_id=tmdb_id))
    return redirect(url_for('tv_detail', tv_id=tmdb_id))
#############################################################################

#############################################################################
# discover routes

@app.route('/discover/movie/<category>')
def discover_movie(category):
    """Display list  of movies based on one of the following categories: popular, top-rated, now-playing, and upcoming

    """
    current_page = request.args.get('page', type=int)
    if category == 'popular':  
        movie_data = api.movie_popular(current_page)
    elif category == 'top-rated':
        movie_data = api.movie_top_rated(current_page)
    elif category == 'now-playing':
        movie_data = api.movie_now_playing(current_page)
    elif category == 'upcoming':
        movie_data = api.movie_upcoming(current_page)
    
        
    return render_template('discover_movies.html',
                            category=category,
                            movie_data=movie_data,
                            current_page=current_page)


@app.route('/discover/tv/<category>')
def discover_tv(category):
    """Display list of TV shows based on one of the following categories: popular, top-rated, on-the-air, and v_airing_today

    """
    current_page = request.args.get('page', type=int)
    if category == 'popular':  
        tv_data = api.tv_popular(current_page)
    elif category == 'top-rated':
        tv_data = api.tv_top_rated(current_page)
    elif category == 'on-the-air':
        tv_data = api.tv_on_the_air(current_page)
    elif category == 'airing-today':
        tv_data = api.tv_airing_today(current_page)
    
        
    return render_template('discover_tv.html',
                            category=category,
                            tv_data=tv_data,
                            current_page=current_page)