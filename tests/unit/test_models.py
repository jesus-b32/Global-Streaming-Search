# import pytest
# from app import app
import os
from flaskr.models import db, User, VideoList, Video, VideoListVideos
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
            assert new_user.password != 'password'
            assert new_user.image_url == '/static/images/default-pic.jpg'
    
    
    class TestVideo:       
        def test_new_video(self, client, new_video):
            """
            GIVEN a User model
            WHEN a new User is created
            THEN check the email and password_hashed fields are defined correctly
            """
            assert new_video.id == 1
            assert new_video.tmdb_id == 2316
            assert new_video.media_type == 'tv'
    
    
    class TestVideoList:        
        def test_video_list(self, client, new_video_list):
            """
            GIVEN a VideoList model
            WHEN a new VideoList is created
            THEN check the user_id and name fields are defined correctly
            """
            assert new_video_list.id == 1
            assert new_video_list.user_id == 1
            assert new_video_list.name == 'favorites'
            
    class TestVideoListVideos:
        def test_adding_video_to_videolist(self, client, add_video_to_list):
            """
            GIVEN a VideoList model
            WHEN a new VideoList is created
            THEN check the user_id and name fields are defined correctly
            """
            assert add_video_to_list.id == 1
            assert add_video_to_list.video_list_id == 1
            assert add_video_to_list.video_id ==  1
            
    class TestRegion:
        def test_new_region(self, client, new_region):
            """
            GIVEN a User model
            WHEN a new User is created
            THEN check the email and password_hashed fields are defined correctly
            """
            assert new_region.id == 'US'
            assert new_region.name == 'United States'

    class TestGenre:
        def test_new_genre(self, client, new_genre):
            """
            GIVEN a User model
            WHEN a new User is created
            THEN check the email and password_hashed fields are defined correctly
            """
            assert new_genre.id == 28
            assert new_genre.name == 'Action'     
            
    class TestGenreList:        
        def test_genre_list(self, client, new_genre_list):
            """
            GIVEN a VideoList model
            WHEN a new VideoList is created
            THEN check the user_id and name fields are defined correctly
            """
            assert new_genre_list.id == 1
            assert new_genre_list.user_id == 1         
            
    class TestGenreListGenres:
        def test_adding_genre_to_genrelist(self, client, add_genre_to_list):
            """
            GIVEN a VideoList model
            WHEN a new VideoList is created
            THEN check the user_id and name fields are defined correctly
            """
            assert add_genre_to_list.id == 1
            assert add_genre_to_list.genre_list_id == 1
            assert add_genre_to_list.genre_id ==  28
            
            
    class TestStreamingProvider:
        def test_streaming_provider(self, client, new_streaming_provider):
            """
            GIVEN a User model
            WHEN a new User is created
            THEN check the email and password_hashed fields are defined correctly
            """
            assert new_streaming_provider.id == 8
            assert new_streaming_provider.name == 'Netflix'     
            assert new_streaming_provider.logo_path == '/pbpMk2JmcoNnQwx5JGpXngfoWtp.jpg'     
            assert new_streaming_provider.display_priority == 5    
            
    class TestStreamingList:        
        def test_streaming_list(self, client, new_streaming_list):
            """
            GIVEN a VideoList model
            WHEN a new VideoList is created
            THEN check the user_id and name fields are defined correctly
            """
            assert new_streaming_list.id == 1
            assert new_streaming_list.user_id == 1         
            
    class TestStreamingListProviders:
        def test_adding_streaming_provider_to_list(self, client, add_streaming_provider_to_list):
            """
            GIVEN a VideoList model
            WHEN a new VideoList is created
            THEN check the user_id and name fields are defined correctly
            """
            assert add_streaming_provider_to_list.id == 1
            assert add_streaming_provider_to_list.streaming_provider_id == 8
            assert add_streaming_provider_to_list.streaming_list_id ==  1            