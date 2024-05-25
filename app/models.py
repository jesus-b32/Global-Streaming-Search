"""SQLAlchemy models for Warbler."""

from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db

from werkzeug.security import check_password_hash, generate_password_hash

from flask_login import UserMixin
from app import login



class User(UserMixin, db.Model):
    """User in the system."""

    __tablename__ = 'users'

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    # email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True, unique=True)
    password_hash: so.Mapped[str] = so.mapped_column(sa.String(256))
    profile_image: so.Mapped[Optional[str]] = so.mapped_column(default="/static/images/default-pic.jpg")
    
    video_lists: so.WriteOnlyMapped['VideoList'] = so.relationship(back_populates='owner')


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


    id: so.Mapped[str] = so.mapped_column(sa.String(3), primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(64))


    def __repr__(self):
        return f"<Country ID: {self.id}, Name:{self.name}>"

#############################################################################
#VIDEOS

#join table
video_list_videos = sa.Table(
    'video_list_videos',
    db.metadata,
    sa.Column('video_id', sa.Integer, sa.ForeignKey('videos.id'), primary_key=True),
    sa.Column('video_list_id', sa.Integer, sa.ForeignKey('video_lists.id'), primary_key=True)
)


class Video(db.Model):
    """An individual message ("warble")."""

    __tablename__ = 'videos'

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    tmdb_id: so.Mapped[int] = so.mapped_column(index=True)
    media_type: so.Mapped[str] = so.mapped_column(sa.String(10), index=True)

    video_lists: so.WriteOnlyMapped['VideoList'] = so.relationship(
        secondary=video_list_videos, 
        back_populates='videos'
    )


    def __repr__(self):
        return f"<Video ID: {self.id}, Media Type: {self.media_type}, TMDB ID: {self.tmdb_id}>"
    
class VideoList(db.Model):
    """An individual message ("warble")."""

    __tablename__ = 'video_lists'

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(64), index=True)

    owner: so.Mapped['User'] = so.relationship(back_populates='video_lists')
    
    videos: so.WriteOnlyMapped['Video'] = so.relationship(
        secondary=video_list_videos, 
        back_populates='video_lists'
    )    


    def __repr__(self):
        return f"<Video List ID: {self.id}, Name: {self.name}, OwnerID: {self.user_id}>"
    
    def video_is_in(self, tmdb_id, media_type):
        query = self.videos.select().where(Video.tmdb_id == tmdb_id, Video.media_type == media_type)
        return db.session.scalar(query) is not None
    
    def add_video(self, video):
        if not self.video_is_in(video.tmdb_id, video.media_type):
            self.videos.add(video)
    
    def remove_video(self, video):
        if self.video_is_in(video.tmdb_id, video.media_type):
            self.videos.remove(video)