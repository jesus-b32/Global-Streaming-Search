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
        
        
if __name__ == '__main__':
    unittest.main(verbosity=2)