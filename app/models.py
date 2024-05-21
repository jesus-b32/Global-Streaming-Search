"""SQLAlchemy models for Warbler."""

# from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db

from werkzeug.security import check_password_hash, generate_password_hash

from flask_login import UserMixin
from app import login



class User(UserMixin, db.Model):
    """User in the system."""

    __tablename__ = 'users'

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    # email = db.Column(
    #     db.Text,
    #     nullable=False,
    #     unique=True,
    # )

    username = db.Column(
        db.Text,
        nullable=False,
        unique=True
    )
    
    password_hash = db.Column(
        db.Text,
        nullable=False
    )    

    profile_image = db.Column(
        db.Text,
        default="/static/images/default-pic.jpg"
    )
    
    video_lists = db.relationship('VideoList', back_populates = 'owner')


    def __repr__(self):
        return f"<User ID: {self.id}, Username: {self.username}>"
    
    # hash the provided password
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
        
    # checked user entered password matches stored password
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    
    @login.user_loader
    def load_user(id):
        return db.session.get(User, int(id))



class Country(db.Model):
    """An individual message ("warble")."""

    __tablename__ = 'countries'

    id = db.Column(
        db.Text,
        primary_key=True,
        nullable=False
    )

    name = db.Column(
        db.Text,
        nullable=False
    )

    def __repr__(self):
        return f"<Country ID: {self.id}, Name:{self.name}>"

#############################################################################
#VIDEOS

#join table
video_list_videos = db.Table(
    'video_list_videos',
    db.Column('video_id', db.Integer, db.ForeignKey('videos.id')),
    db.Column('video_list_id', db.Integer, db.ForeignKey('video_lists.id'))
)


class Video(db.Model):
    """An individual message ("warble")."""

    __tablename__ = 'videos'
    
    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )    

    tmdb_id = db.Column(
        db.Integer,
        nullable=False
    )    

    media_type = db.Column(
        db.Text,
        nullable=False
    )
    
    video_lists = db.relationship(
        'VideoList', 
        secondary = 'video_list_videos',
        back_populates = 'videos'
    )

    def __repr__(self):
        return f"<Video ID: {self.id}, Media Type: {self.media_type}, TMDB ID: {self.tmdb_id}>"
    
class VideoList(db.Model):
    """An individual message ("warble")."""

    __tablename__ = 'video_lists'

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False
    )

    name = db.Column(
        db.Text,
        nullable=False
    )
    
    owner = db.relationship('User', back_populates = 'video_lists')
    
    # videos = db.relationship('VideoListVideos')
    
    videos = db.relationship(
        'Video',
        secondary = 'video_list_videos',
        back_populates = 'video_lists'
    )

    def __repr__(self):
        return f"<Video List ID: {self.id}, Name: {self.name}, OwnerID: {self.user_id}>"





# class VideoListVideos(db.Model):
#     """An individual message ("warble")."""
#     __tablename__  = 'video_list_videos'
#     id = db.Column(db.Integer,
#                     primary_key=True,
#                     autoincrement=True)    
#     video_list_id = db.Column(db.Integer,
#                             db.ForeignKey('video_lists.id'),
#                             primary_key=True,
#                             nullable=False
#                             )
#     tmdb_id = db.Column(db.Integer,
#                         primary_key=True, 
#                         nullable=False 
#                         )
#     media_type = db.Column(db.Text,
#                         primary_key=True, 
#                         nullable=False 
#                         )
    
    # video_list = db.relationship('VideoList')    
#############################################################################

############################################################################
#GENRES
# class Genre(db.Model):
#     """An individual message ("warble")."""

#     __tablename__ = 'genres'

#     id = db.Column(
#         db.Integer,
#         primary_key=True,
#         nullable=False,
#     )

#     name = db.Column(
#         db.Text,
#         nullable=False,
#     )
#     genre_lists = db.relationship(
#         'GenreList',
#         secondary = 'genre_list_genres',
#         back_populates = 'genres'
#         )

#     def __repr__(self):
#         return f"<Genre #{self.id}: {self.name}>"

# class GenreList(db.Model):
#     """An individual message ("warble")."""

#     __tablename__ = 'genre_lists'

#     id = db.Column(
#         db.Integer,
#         primary_key=True,
#         autoincrement=True,
#     )

#     user_id = db.Column(
#         db.Integer,
#         db.ForeignKey('users.id', ondelete='CASCADE'),
#         nullable=False,
#     )
    
#     genres = db.relationship(
#         'Genre',
#         secondary = 'genre_list_genres',
#         back_populates = 'genre_lists'
#     )

#     def __repr__(self):
#         return f"<List #{self.id}: {self.name}, {self.user_id}>"


# #join table
# class GenreListGenres(db.Model):
#     'genre_list_genres'
#     __tablename__ = 'genre_list_genres'
#     id = db.Column(db.Integer,
#                     primary_key=True,
#                     autoincrement=True)       
#     genre_id = db.Column(db.Integer, 
#                         db.ForeignKey('genres.id'))
#     genre_list_id = db.Column(db.Integer, 
#                         db.ForeignKey('genre_lists.id'))

# ####################################################################################

# #####################################################################################
# #STREAMING PROVIDERS
# class StreamingProvider(db.Model):
#     """An individual message ("warble")."""

#     __tablename__ = 'streaming_providers'

#     id = db.Column(
#         db.Integer,
#         primary_key=True,
#         nullable=False,
#     )

#     name = db.Column(
#         db.Text,
#         nullable=False,
#     )

#     logo_path = db.Column(
#         db.Text,
#         nullable=False,
#     )

#     display_priority = db.Column(
#         db.Integer,
#         nullable=False,
#     )
    
#     streaming_lists = db.relationship(
#         'StreamingList',
#         secondary = 'streaming_list_providers',
#         back_populates = 'streaming_providers'
#     )    

#     def __repr__(self):
#         return f"<Streaming_service #{self.id}: {self.name}>"

# class StreamingList(db.Model):
#     """An individual message ("warble")."""

#     __tablename__ = 'streaming_lists'

#     id = db.Column(
#         db.Integer,
#         primary_key=True,
#         autoincrement=True,
#     )

#     user_id = db.Column(
#         db.Integer,
#         db.ForeignKey('users.id', ondelete='CASCADE'),
#         nullable=False,
#     )
    
#     streaming_providers = db.relationship(
#         'StreamingProvider',
#         secondary = 'streaming_list_providers',
#         back_populates = 'streaming_lists'
#     )

#     def __repr__(self):
#         return f"<List #{self.id}: {self.name}, {self.user_id}>"


# #join table
# class StreamingListProviders(db.Model):
#     'streaming_list_providers'
#     __tablename__ = 'streaming_list_providers'
#     id = db.Column(db.Integer,
#                     primary_key=True,
#                     autoincrement=True)      
#     streaming_provider_id = db.Column(db.Integer, db.ForeignKey('streaming_providers.id'))
#     streaming_list_id = db.Column(db.Integer, db.ForeignKey('streaming_lists.id'))
    

#####################################################################################

#####################################################################################
#PEOPLE
# class Person(db.Model):
#     """An individual message ("warble")."""

#     __tablename__ = 'persons'

#     id = db.Column(
#         db.Integer,
#         primary_key=True,
#         nullable=False,
#     )
#     person_lists = db.relationship(
#         'PersonList',
#         secondary = 'person_list_persons',
#         back_populates = 'persons'
#     )    

#     def __repr__(self):
#         return f"<Person #{self.id}>"
    
    
# class PersonList(db.Model):
#     """An individual message ("warble")."""

#     __tablename__ = 'person_lists'

#     id = db.Column(
#         db.Integer,
#         primary_key=True,
#         autoincrement=True,
#     )

#     user_id = db.Column(
#         db.Integer,
#         db.ForeignKey('users.id', ondelete='CASCADE'),
#         nullable=False,
#     )
    
#     person = db.relationship(
#         'Person',
#         secondary = 'person_list_persons',
#         back_populates = 'person_lists'
#     )

#     def __repr__(self):
#         return f"<List #{self.id}: {self.name}, {self.user_id}>"


# #join table
# person_list_persons = db.Table(
#     'person_list_persons',
#     db.Column('person_id', db.Integer, db.ForeignKey('persons.id')),
#     db.Column('person_list_id', db.Integer, db.ForeignKey('person_lists.id'))
# )