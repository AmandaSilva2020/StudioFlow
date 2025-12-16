from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo, length, Regexp, Optional

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired('Missing username'), length(min=3, max=30), Regexp (r'^\S+$', message='Username must not contain spaces')])

    password = PasswordField('Password', validators=[DataRequired('Missing password'), length(min=6, max=8, message='Password must have 6 to 8 characteres'), Regexp (r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[\W_]).+$', message='Password must contain at least one uppercase letter, one lowercase letter, one digit, and one special character')])

    confirmation = PasswordField('Confirm Password', validators=[DataRequired('Missing confirmation'), EqualTo('password', message='Passwords must match')])

    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired('Missing username')])
    password = PasswordField('Password', validators=[DataRequired('Missing password')])
    submit = SubmitField('Log In')

class ProfileForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(message="Missing username."), Regexp(r'^\S+$', message="Username must not contain spaces"), length(min=3, max=30, message="Username must have 3 to 30 characters.")])

    current_password = PasswordField("Current password", validators=[Optional()])

    new_password = PasswordField("New password", validators=[Optional(), length(min=6, max=8, message="Password must have 6 to 8 characteres"), Regexp( r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[\W_]).+$', message="Password must contain at least one uppercase letter, one lowercase letter, one digit, and one special character")])

    confirmation = PasswordField("Confirm new password", validators=[Optional()])

    submit = SubmitField("Save Changes")
