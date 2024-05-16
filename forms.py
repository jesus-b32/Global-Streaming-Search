from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length


# class MessageForm(FlaskForm):
#     """Form for adding/editing messages."""

#     text = TextAreaField('text', validators=[DataRequired()])


class UserAddForm(FlaskForm):
    """Form for adding users."""

    username = StringField('Username', validators=[DataRequired()])
    # email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[Length(min=6)])
    profile_image = StringField('Image URL (Optional)')
    # submit = SubmitField('Sign In')


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