from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class SignInForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password')
    remember_me = BooleanField('remember_me')
    signin = SubmitField('sign in')
