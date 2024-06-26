""" 
Seed database with configuration data from TMDB API. Do this you need run flask shell command. From there import seed.py like this: import app.seed as seed. From there run the function to seed database table. EX: seed.fill_country_table()
"""

from app import db
from app.models import Country, User, Video, VideoList
import app.api as api

##### Filling the Country table ######################

def fill_country_table():
    countries = api.all_countries()
    for country in countries:
        new_country = Country(
            id = country['iso_3166_1'],
            name = country['native_name']
            )
        db.session.add(new_country)
    db.session.commit()
########################################################



##### Adding Users ######################

def add_users():
    user1 = User(username='test1')
    user1.set_password('password1')
    
    # user2 = User(username='test2')
    # user2.set_password('password2')    
    
    # db.session.add_all([user1, user2])
    db.session.add(user1)
    db.session.commit()
    
    return user1
########################################################



##### Adding videos ######################

def add_videos():
    video1 = Video(tmdb_id=2316, media_type = 'tv')
    
    video2 = Video(tmdb_id=272, media_type = 'movie')
    
    db.session.add_all([video1, video2])
    db.session.commit()
    
    return [video1, video2]
########################################################



##### Adding videolists ######################

def add_video_lists(user_id):
    watchlist = VideoList(user_id=user_id, name = 'watchlist')
    
    # favorites = VideoList(user_id=user_id, name = 'favorites')
    
    # db.session.add_all([watchlist, favorites])
    db.session.add(watchlist)
    db.session.commit()
    
    return watchlist
########################################################


##### Adding videos to video list ######################

def add_video_to_video_list(video, watchlist):
    # watchlist = VideoList(user_id=user_id, name = 'watchlist')
    
    watchlist.videos.add(video)
    db.session.commit()
########################################################


