# import pytest
# from app import app
import os
from flaskr.models import db, User, VideoList, Video
os.environ['DATABASE_URL'] = "postgresql:///global-streaming-search-test"

# Now we can import app
from flaskr.app import app


class TestModels:
    class TestUser:
        def test_new_user(self, client, new_user):
            """
            GIVEN a User model
            WHEN a new User is created
            THEN check the email and password_hashed fields are defined correctly
            """            
            assert new_user.id == 1
            assert new_user.email == 'test@gmail.com'
            assert new_user.username == 'test1'
            assert new_user.password_hashed != 'password'
    
    
    class TestVideo:       
        def test_new_video(self, client, new_video):
            """
            GIVEN a User model
            WHEN a new User is created
            THEN check the email and password_hashed fields are defined correctly
            """
            # assert new_video.get((2316, 'tv')) == 2316
            assert new_video == 'tv'
    
    
    # class TestVideoList:        
    #     def test_video_list(self, client, new_video_list):
    #         """
    #         GIVEN a VideoList model
    #         WHEN a new VideoList is created
    #         THEN check the user_id and name fields are defined correctly
    #         """
    #         assert new_video_list.user_id == 1
    #         assert new_video_list.name == 'favorites'
    
        # def test_adding_video_to_videolist(self, new_video_list, new_user, new_video):
        #     """
        #     GIVEN a VideoList model
        #     WHEN a new VideoList is created
        #     THEN check the user_id and name fields are defined correctly
        #     """
        #     new_video_list.videos.append(new_video)
        #     print(f'video id {new_video_list.videos[0].id} is in video list')
        #     assert new_video_list.videos[0].id == new_video.id
        #     assert new_video_list.videos[0].media_type == new_video.media_type
            
        #     assert new_video.video_lists[0].id == new_video_list.id
        #     assert new_video.video_lists[0].user_id == new_user.id
        #     assert new_video.video_lists[0].name == new_video_list.name