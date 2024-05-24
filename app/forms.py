from flask_wtf import FlaskForm
from flask_wtf.form import _Auto
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
import sqlalchemy as sa
from app import db
from app.models import User


class UserRegisterForm(FlaskForm):
    """Form for adding users."""

    username = StringField('Username', validators=[DataRequired()])
    # email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    profile_image = StringField('Image URL (Optional)')
    # submit = SubmitField('Sign In')
    
    def validate_username(self, username):
        user = db.session.scalar(sa.select(User).where(User.username == username.data))
        if user is not None:
            raise ValidationError('Please user a different username')


class LoginForm(FlaskForm):
    """Login form."""

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])
    remember_me = BooleanField('Remember Me')



class EditProfileForm(FlaskForm):
    """Form for editing  user profile."""

    username = StringField('Username', validators=[DataRequired()])
    # email = StringField('E-mail', validators=[DataRequired(), Email()])
    profile_image = StringField('Profile Image URL (Optional)')
    # password = PasswordField('Password', validators=[Length(min=6)])
    
    def __init__(self, original_username, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.original_username = original_username
        
    def validate_username(self, username):
        if username.data != self.original_username:
            user = db.session.scalar(sa.select(User).where(User.username == self.username.data))
        if user is not None:
            raise ValidationError('Please user a different username')