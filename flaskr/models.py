"""SQLAlchemy models for Warbler."""

# from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
# from sqlalchemy.schema import PrimarykeyConstraint
#from werkzeug.security import check_password_hash, generate_password_hash
# from flask_security import Security, SQLAlchemyUserDatastore, auth_required, hash_password
# from flask_security.models import fsqla_v3 as fsqla

bcrypt = Bcrypt()
db = SQLAlchemy()


def connect_db(app):
    """Connect this database to provided Flask app.

    You should call this in your Flask app.
    """

    db.app = app
    db.init_app(app)
    


class User(db.Model):
    """User in the system."""

    __tablename__ = 'users'

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True,
    )

    email = db.Column(
        db.Text,
        nullable=False,
        unique=True,
    )

    username = db.Column(
        db.Text,
        nullable=False,
        unique=True,
    )
    
    password_hashed = db.Column(
        db.Text,
        nullable=False,
    )    

    # image_url = db.Column(
    #     db.Text,
    #     # default="/static/images/default-pic.png",
    # )

    def __init__(self, email, username, password_hashed):
        self.email = email
        self.username = username
        self.password_hashed = self.password_hashing(password_hashed)
        
    @staticmethod
    def password_hashing(password_plaintext):
        return bcrypt.generate_password_hash(password_plaintext).decode('UTF-8')
        


    def __repr__(self):
        return f"<User #{self.id}: {self.username}, {self.email}>"

    @classmethod
    def signup(cls, username, email, password, image_url):
        """Sign up user.

        Hashes password and adds user to system.
        """

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            username=username,
            email=email,
            password=hashed_pwd,
            image_url=image_url,
        )

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):
        """Find user with `username` and `password`.

        This is a class method (call it on the class, not an individual user.)
        It searches for a user whose password hash matches this password
        and, if it finds such a user, returns that user object.

        If can't find matching user (or if password is wrong), returns False.
        """

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False
    
    @classmethod
    def check_password(cls, username, password):
        """Check if entered password by user matches passord stored.

        This is a class method (call it on the class, not an individual user.)
        It checks if the password entered by user whose password hash matches this password. Returns true if matches and false if it does not.
        """

        user = cls.query.filter_by(username=username).first()

        if user:
            return bcrypt.check_password_hash(user.password, password)


class Region(db.Model):
    """An individual message ("warble")."""

    __tablename__ = 'regions'

    id = db.Column(
        db.Text,
        primary_key=True,
        nullable=False,
    )

    name = db.Column(
        db.Text,
        nullable=False,
    )

    def __repr__(self):
        return f"<Region #{self.id}: {self.name}>"

#############################################################################
#VIDEOS
class Video(db.Model):
    """An individual message ("warble")."""

    __tablename__ = 'videos'
    
    id = db.Column(
        db.Integer,
        primary_key=True,
        nullable=False,
    )    

    tmdb_id = db.Column(
        db.Integer,
        nullable=False,
    )    

    media_type = db.Column(
        db.Text,
        nullable=False,
    )
    
    video_lists = db.relationship(
        'VideoList', 
        secondary = 'video_list_videos',
        back_populates = 'videos'
    )



    def __repr__(self):
        return f"<Video #{self.id}: {self.media_type} and {self.tmdb_id}>"
    
class VideoList(db.Model):
    """An individual message ("warble")."""

    __tablename__ = 'video_lists'

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True,
        unique=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False,
    )

    name = db.Column(
        db.Text,
        nullable=False,
    )
    
    videos = db.relationship(
        'Video',
        secondary = 'video_list_videos',
        back_populates = 'video_lists'
    )

    def __repr__(self):
        return f"<List #{self.id}: {self.name}, {self.user_id}>"


#association table
class VideoListVideos(db.Model):
    """An individual message ("warble")."""
    __tablename__  = 'video_list_videos'
    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)    
    video_list_id = db.Column(db.Integer, 
                            db.ForeignKey('video_lists.id'),
                            nullable=False 
                            # primary_key=True
                            )
    video_id = db.Column(db.Integer, 
                        db.ForeignKey('videos.id'),
                        nullable=False 
                        # primary_key=True
                        )
# video_list_videos = db.Table(
#     'video_list_videos',
#     db.Column('video_list_id', db.Integer, db.ForeignKey('video_lists.id'), primary_key=True),
#     db.Column('video_id', db.Integer, db.ForeignKey('videos.id'),primary_key=True)
# )
#############################################################################

############################################################################
#GENRES
class Genre(db.Model):
    """An individual message ("warble")."""

    __tablename__ = 'genres'

    id = db.Column(
        db.Integer,
        primary_key=True,
        nullable=False,
    )

    name = db.Column(
        db.Text,
        nullable=False,
    )
    genre_lists = db.relationship(
        'GenreList',
        secondary = 'genre_list_genres',
        back_populates = 'genres'
        )

    def __repr__(self):
        return f"<Genre #{self.id}: {self.name}>"

class GenreList(db.Model):
    """An individual message ("warble")."""

    __tablename__ = 'genre_lists'

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True,
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False,
    )
    
    genres = db.relationship(
        'Genre',
        secondary = 'genre_list_genres',
        back_populates = 'genre_lists'
    )

    def __repr__(self):
        return f"<List #{self.id}: {self.name}, {self.user_id}>"


#join table
genre_list_genres = db.Table(
    'genre_list_genres',
    db.Column('genre_id', db.Integer, db.ForeignKey('genres.id')),
    db.Column('genre_list_id', db.Integer, db.ForeignKey('genre_lists.id'))
)
####################################################################################

#####################################################################################
#STREAMING PROVIDERS
class StreamingProvider(db.Model):
    """An individual message ("warble")."""

    __tablename__ = 'streaming_providers'

    id = db.Column(
        db.Integer,
        primary_key=True,
        nullable=False,
    )

    name = db.Column(
        db.Text,
        nullable=False,
    )

    logo_path = db.Column(
        db.Text,
        nullable=False,
    )

    display_priority = db.Column(
        db.Integer,
        nullable=False,
    )
    
    streaming_lists = db.relationship(
        'StreamingList',
        secondary = 'streaming_list_providers',
        back_populates = 'streaming_providers'
    )    

    def __repr__(self):
        return f"<Streaming_service #{self.id}: {self.name}>"

class StreamingList(db.Model):
    """An individual message ("warble")."""

    __tablename__ = 'streaming_lists'

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True,
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False,
    )
    
    streaming_providers = db.relationship(
        'StreamingProvider',
        secondary = 'streaming_list_providers',
        back_populates = 'streaming_lists'
    )

    def __repr__(self):
        return f"<List #{self.id}: {self.name}, {self.user_id}>"


#join table
streaming_list_providers = db.Table(
    'streaming_list_providers',
    db.Column('streaming_provider_id', db.Integer, db.ForeignKey('streaming_providers.id')),
    db.Column('streaming_list_id', db.Integer, db.ForeignKey('streaming_lists.id'))
)
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










# class Follows(db.Model):
#     """Connection of a follower <-> followed_user."""

#     __tablename__ = 'follows'

#     user_being_followed_id = db.Column(
#         db.Integer,
#         db.ForeignKey('users.id', ondelete="cascade"),
#         primary_key=True,
#     )

#     user_following_id = db.Column(
#         db.Integer,
#         db.ForeignKey('users.id', ondelete="cascade"),
#         primary_key=True,
#     )


# class Likes(db.Model):
#     """Mapping user likes to warbles."""

#     __tablename__ = 'likes' 

#     id = db.Column(
#         db.Integer,
#         primary_key=True
#     )

#     user_id = db.Column(
#         db.Integer,
#         db.ForeignKey('users.id', ondelete='cascade')
#     )

#     message_id = db.Column(
#         db.Integer,
#         db.ForeignKey('messages.id', ondelete='cascade'),
#         unique=True
#     )


# class User(db.Model):
#     """User in the system."""

#     __tablename__ = 'users'

#     id = db.Column(
#         db.Integer,
#         primary_key=True,
#     )

#     email = db.Column(
#         db.Text,
#         nullable=False,
#         unique=True,
#     )

#     username = db.Column(
#         db.Text,
#         nullable=False,
#         unique=True,
#     )

#     image_url = db.Column(
#         db.Text,
#         default="/static/images/default-pic.png",
#     )

#     header_image_url = db.Column(
#         db.Text,
#         default="/static/images/warbler-hero.jpg"
#     )

#     bio = db.Column(
#         db.Text,
#     )

#     location = db.Column(
#         db.Text,
#     )

#     password = db.Column(
#         db.Text,
#         nullable=False,
#     )

#     messages = db.relationship('Message')

#     followers = db.relationship(
#         "User",
#         secondary="follows",
#         primaryjoin=(Follows.user_being_followed_id == id),
#         secondaryjoin=(Follows.user_following_id == id)
#     )

#     following = db.relationship(
#         "User",
#         secondary="follows",
#         primaryjoin=(Follows.user_following_id == id),
#         secondaryjoin=(Follows.user_being_followed_id == id)
#     )

#     #like will hold a list of messages objects.
#     #the relation with Like table append current user id and message id
#     likes = db.relationship(
#         'Message',
#         secondary="likes"
#     )

#     def __repr__(self):
#         return f"<User #{self.id}: {self.username}, {self.email}>"

#     def is_followed_by(self, other_user):
#         """Is this user followed by `other_user`?"""

#         found_user_list = [user for user in self.followers if user == other_user]
#         return len(found_user_list) == 1

#     def is_following(self, other_user):
#         """Is this user following `other_use`?"""

#         found_user_list = [user for user in self.following if user == other_user]
#         return len(found_user_list) == 1

#     @classmethod
#     def signup(cls, username, email, password, image_url):
#         """Sign up user.

#         Hashes password and adds user to system.
#         """

#         hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

#         user = User(
#             username=username,
#             email=email,
#             password=hashed_pwd,
#             image_url=image_url,
#         )

#         db.session.add(user)
#         return user

#     @classmethod
#     def authenticate(cls, username, password):
#         """Find user with `username` and `password`.

#         This is a class method (call it on the class, not an individual user.)
#         It searches for a user whose password hash matches this password
#         and, if it finds such a user, returns that user object.

#         If can't find matching user (or if password is wrong), returns False.
#         """

#         user = cls.query.filter_by(username=username).first()

#         if user:
#             is_auth = bcrypt.check_password_hash(user.password, password)
#             if is_auth:
#                 return user

#         return False
    
#     @classmethod
#     def check_password(cls, username, password):
#         """Check if entered password by user matches passord stored.

#         This is a class method (call it on the class, not an individual user.)
#         It checks if the password entered by user whose password hash matches this password. Returns true if matches and false if it does not.
#         """

#         user = cls.query.filter_by(username=username).first()

#         if user:
#             return bcrypt.check_password_hash(user.password, password)


# class Message(db.Model):
#     """An individual message ("warble")."""

#     __tablename__ = 'messages'

#     id = db.Column(
#         db.Integer,
#         primary_key=True,
#     )

#     text = db.Column(
#         db.String(140),
#         nullable=False,
#     )

#     timestamp = db.Column(
#         db.DateTime,
#         nullable=False,
#         default=datetime.utcnow(),
#     )

#     user_id = db.Column(
#         db.Integer,
#         db.ForeignKey('users.id', ondelete='CASCADE'),
#         nullable=False,
#     )

#     user = db.relationship('User')

#     def __repr__(self):
#         return f"<Message #{self.id}: {self.text}, {self.user_id}>"

    
#     def is_liked(self, user):
#         """Check if current message is in a user's liked list"""

#         found_liked_msg = [msg for msg in user.likes if msg == self]
#         return len(found_liked_msg) == 1