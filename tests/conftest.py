import os
import pytest
# from app import app
from flaskr.models import db, User, VideoList, Video
# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///global-streaming-search-test"

# Now we can import app
from flaskr.app import app


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
        email='test@gmail.com', 
        username='test1',
        password_hashed='password'
        )
    with app.app_context():
        db.session.add(user)
        db.session.commit()
        fetched_user = User.query.get(user.id)       
    
    return fetched_user

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
        fetched_video_list = VideoList.query.get(video_list.id)    

    return fetched_video_list


@pytest.fixture() 
def new_video():
    """
    
    """
    video = Video(
        id = 2316, 
        media_type='tv'
        )
    with app.app_context():
        db.session.add(video)
        db.session.commit()
        # fetched_video_list = VideoList.query.get(video.id)
        # fetched_video = Video.query.get()
        # fetched_video = Video.query.filter((Video.id, Video.media_type) == (2316, 'tv')).first()        
        # fetched_video = Video.query.filter((Video.id == 2316) & (Video.media_type == 'tv'))
        fetched_video = Video.query.filter_by(id=2316, media_type='tv')

    return fetched_video