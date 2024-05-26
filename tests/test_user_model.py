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
from app.models import User, Country, VideoList, Video


class UserModelCase(unittest.TestCase):
    def setUp(self):
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()
        
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
        
    def test_password_hashing(self):
        user = User(username='john')
        user.set_password('password')
        
        self.assertFalse(user.check_password('password123'))
        self.assertTrue(user.check_password('password'))
        
    def test_video_lists_relationship(self):
        user = User(username='john')
        user.set_password('password')
        db.session.add(user)
        db.session.commit()
        
        video_list = VideoList(user_id=user.id, name='watchlist')
        db.session.add(video_list)
        db.session.commit()
                
        query = user.video_lists.select().where(VideoList.name == 'watchlist')
        user_watchlist = db.session.scalar(query)
        
        self.assertTrue(video_list.owner == user)
        self.assertTrue(user_watchlist == video_list)        
        
        
if __name__ == '__main__':
    unittest.main(verbosity=2)