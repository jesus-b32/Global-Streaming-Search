import os, sys
os.environ['DATABASE_URL'] = "postgresql:///global-streaming-search-test"

##This section adds the parent directory(capstone 1 directory) to the current system path

# getting the name of the directory where this file is present.(tests)
current = os.path.dirname(os.path.realpath(__file__))

# Getting the parent directory name where the current directory is present.
parent = os.path.dirname(current)

# adding the parent directory to the sys.path.
sys.path.append(parent)
#####################################################################################

import unittest
from app import app, db
import sqlalchemy as sa
from app.models import User, VideoList, Video



class VideoListModelCase(unittest.TestCase):
    def setUp(self):
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()      
        
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
        
    def test_video_is_in(self):
        user = User(username='john')
        user.set_password('password')
        db.session.add(user)
        db.session.commit()
        
        the_office = Video(tmdb_id=2316, media_type='tv')
        glass = Video(tmdb_id=450465, media_type='movie')
        db.session.add_all([the_office, glass])
        db.session.commit()
        
        video_list = VideoList(user_id=user.id, name='watchlist')
        db.session.add(video_list)
        db.session.commit()
        
        video_list.videos.add(the_office)
        db.session.commit()  
        
        self.assertTrue(video_list.video_is_in(the_office.tmdb_id, the_office.media_type))
        self.assertFalse(video_list.video_is_in(glass.tmdb_id, glass.media_type))
        
    def test_add_video(self):
        user = User(username='john')
        user.set_password('password')
        db.session.add(user)
        db.session.commit()
        
        the_office = Video(tmdb_id=2316, media_type='tv')
        dune = Video(tmdb_id=438631, media_type='movie')
        db.session.add_all([the_office, dune])
        db.session.commit()
        
        video_list = VideoList(user_id=user.id, name='watchlist')
        db.session.add(video_list)
        db.session.commit()
        
        video_list.add_video(the_office)     
        db.session.commit()  
        
        self.assertTrue(video_list.video_is_in(the_office.tmdb_id, the_office.media_type))
        self.assertFalse(video_list.video_is_in(dune.tmdb_id, dune.media_type))
        
    def test_remove_video(self):
        user = User(username='john')
        user.set_password('password')
        db.session.add(user)
        db.session.commit()
        
        the_office = Video(tmdb_id=2316, media_type='tv')
        dune = Video(tmdb_id=438631, media_type='movie')
        db.session.add_all([the_office, dune])
        db.session.commit()
        
        video_list = VideoList(user_id=user.id, name='watchlist')
        db.session.add(video_list)
        db.session.commit()
        
        video_list.add_video(the_office)     
        video_list.add_video(dune)     
        db.session.commit()
        
        video_list.remove_video(the_office)     
        db.session.commit()  
        
        self.assertFalse(video_list.video_is_in(the_office.tmdb_id, the_office.media_type))
        self.assertTrue(video_list.video_is_in(dune.tmdb_id, dune.media_type))
        
    def test_video_lists_relationship(self):
        user = User(username='john')
        user.set_password('password')
        db.session.add(user)
        db.session.commit()
        
        the_office = Video(tmdb_id=2316, media_type='tv')
        db.session.add(the_office)
        db.session.commit()
        
        video_list = VideoList(user_id=user.id, name='watchlist')
        db.session.add(video_list)
        db.session.commit()
        
        video_list.add_video(the_office)     
        db.session.commit()
        
        query = video_list.videos.select().where(Video.tmdb_id == the_office.tmdb_id, Video.media_type == the_office.media_type)
        watchlist_video = db.session.scalar(query)                  
                
        self.assertTrue(watchlist_video == the_office)
        
        
        
if __name__ == '__main__':
    unittest.main(verbosity=2)