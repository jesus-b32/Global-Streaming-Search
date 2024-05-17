from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
import sqlalchemy as sa
from app import db
from models import User


# class MessageForm(FlaskForm):
#     """Form for adding/editing messages."""

#     text = TextAreaField('text', validators=[DataRequired()])


class UserRegisterForm(FlaskForm):
    """Form for adding users."""

    username = StringField('Username', validators=[DataRequired()])
    # email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    password2 = PasswordField('Repeate Password', validators=[DataRequired(), EqualTo('password')])
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



class UserEditForm(FlaskForm):
    """Form for editing  user profile."""

    username = StringField('Username', validators=[DataRequired()])
    # email = StringField('E-mail', validators=[DataRequired(), Email()])
    profile_image = StringField('Image URL (Optional)')
    # header_image_url = StringField('Header Image URL (Optional)')
    # bio = StringField('Bio (Optional)')
    password = PasswordField('Password', validators=[Length(min=6)])