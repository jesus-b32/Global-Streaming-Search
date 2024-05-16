import os
import pytest
# from app import app
from models import db, User, VideoList, Video, VideoListVideos, Region

# Genre, GenreList, GenreListGenres, StreamingProvider, StreamingList, StreamingListProviders


# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///global-streaming-search-test"

# Now we can import app
from app import app


# @pytest.fixture()
# def app_setup():
#     app.config['TESTING'] = True
#     app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#     app.config['SQLALCHEMY_ECHO'] = False
#     # Don't have WTForms use CSRF at all, since it's a pain to test
#     app.config['WTF_CSRF_ENABLED'] = False

#     # This is a bit of hack, but don't use Flask DebugToolbar
#     app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']
            
#     return app

@pytest.fixture()
def client():
    # Create our tables (we do this here, so we only create the tables
    # once for all tests --- in each test, we'll delete the data
    # and create fresh new clean test data
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ECHO'] = False
    # Don't have WTForms use CSRF at all, since it's a pain to test
    app.config['WTF_CSRF_ENABLED'] = False

    # This is a bit of hack, but don't use Flask DebugToolbar
    app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
    # other setup can go here
    
        yield client

    # clean up / reset resources here
        with app.app_context():
            db.session.remove()
            db.close_all_sessions()
            db.drop_all()

# module - run once per module (e.g., a test file)
@pytest.fixture() 
def new_user():
    """
    
    """
    user = User(
        # email='test@gmail.com', 
        username='test1',
        password='password',
        profile_image=None
        )
    with app.app_context():
        db.session.add(user)
        db.session.commit()
        fetched_user = db.session.get(User, user.id)          
    
    return fetched_user


@pytest.fixture() 
def new_video():
    """
    
    """
    video = Video(
        tmdb_id = 2316, 
        media_type='tv'
        )
    with app.app_context():
        db.session.add(video)
        db.session.commit()
        fetched_video = db.session.get(Video, video.id)

    return fetched_video


@pytest.fixture() 
def new_video_list(new_user):
    """
    
    """
    video_list = VideoList(
        user_id = new_user.id, 
        name='favorites'
        )
    with app.app_context():
        db.session.add(video_list)
        db.session.commit()
        fetched_video_list = db.session.get(VideoList, video_list.id)
    return fetched_video_list


@pytest.fixture() 
def add_video_to_list():
# def add_video_to_list(new_user, new_video, new_video_list):
    """
    
    """
    user = User(
        # email='test@gmail.com', 
        username='test1',
        password='password',
        profile_image=None
        
        )
    video = Video(
        tmdb_id = 2316, 
        media_type='tv'
        )
    video_list = VideoList(
        user_id = 1, 
        name='favorites'
        )
    with app.app_context():
        db.session.add_all([user, video, video_list])
        db.session.commit()    
        video_list_videos = VideoListVideos(
                            video_list_id = video_list.id,
                            video_id = video.id)
    
            
    with app.app_context():
        db.session.add(video_list_videos)
        db.session.commit()
        fetched_video_list = db.session.get(VideoListVideos, video_list_videos.id) 
    return fetched_video_list

@pytest.fixture() 
def new_region():
    """
    
    """
    region = Region(
        id='US', 
        name='United States'
        )
    with app.app_context():
        db.session.add(region)
        db.session.commit()
        fetched_region = db.session.get(Region, 'US')          
    
    return fetched_region


# @pytest.fixture() 
# def new_genre():
#     """
    
#     """
#     genre = Genre(
#         id= 28, 
#         name='Action'
#         )
#     with app.app_context():
#         db.session.add(genre)
#         db.session.commit()
#         fetched_genre = db.session.get(Genre, 28)          
    
#     return fetched_genre


# @pytest.fixture() 
# def new_genre_list(new_user):
#     """
    
#     """
#     genre_list = GenreList(
#         user_id = new_user.id
#         )
#     with app.app_context():
#         db.session.add(genre_list)
#         db.session.commit()
#         fetched_genre_list = db.session.get(GenreList, genre_list.id)
#     return fetched_genre_list

# @pytest.fixture() 
# def add_genre_to_list(new_genre, new_genre_list):
# # def add_video_to_list(new_user, new_video, new_video_list):
#     """
    
#     """

#     genre_list_genres = GenreListGenres(
#                             genre_id = new_genre.id,
#                             genre_list_id = new_genre_list.id)
    
            
#     with app.app_context():
#         db.session.add(genre_list_genres)
#         db.session.commit()
#         fetched_genre_list_genres = db.session.get(GenreListGenres, genre_list_genres.id) 
#     return fetched_genre_list_genres


# @pytest.fixture() 
# def new_streaming_provider():
#     """
    
#     """
#     streaming_provider = StreamingProvider(
#         id= 8, 
#         name='Netflix',
#         logo_path = '/pbpMk2JmcoNnQwx5JGpXngfoWtp.jpg',
#         display_priority = 5
#         )
#     with app.app_context():
#         db.session.add(streaming_provider)
#         db.session.commit()
#         fetched_streaming_provider = db.session.get(StreamingProvider, 8)          
    
#     return fetched_streaming_provider


# @pytest.fixture() 
# def new_streaming_list(new_user):
#     """
    
#     """
#     streaming_list = StreamingList(
#         user_id = new_user.id
#         )
#     with app.app_context():
#         db.session.add(streaming_list)
#         db.session.commit()
#         fetched_streaming_list = db.session.get(StreamingList, streaming_list.id)
#     return fetched_streaming_list

# @pytest.fixture() 
# def add_streaming_provider_to_list(new_streaming_provider, new_streaming_list):
# # def add_video_to_list(new_user, new_video, new_video_list):
#     """
    
#     """

#     streaming_list_providers = StreamingListProviders(
#                             streaming_provider_id = new_streaming_provider.id,
#                             streaming_list_id = new_streaming_list.id)
    
            
#     with app.app_context():
#         db.session.add(streaming_list_providers)
#         db.session.commit()
#         fetched_genre_list_genres = db.session.get(StreamingListProviders, streaming_list_providers.id) 
#     return fetched_genre_list_genres