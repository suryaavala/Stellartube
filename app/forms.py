from flask_wtf import FlaskForm
import wtforms as wtf

class SignInForm(FlaskForm):
    username = wtf.StringField(
        'username',
        validators=[wtf.validators.DataRequired()]
    )
    password = wtf.PasswordField(
        'password',
        validators=[wtf.validators.DataRequired()]
    )
    remember_me = wtf.BooleanField('remember me')
    submit = wtf.SubmitField('submit')

class SignUpForm(FlaskForm):
    username = wtf.StringField(
        'username',
        validators=[wtf.validators.DataRequired()]
    )
    password = wtf.PasswordField(
        'password', 
        validators=[wtf.validators.DataRequired()]
    )
    confirm_password = wtf.PasswordField('confirm password')
    address = wtf.StringField(
        'address',
        validators=[wtf.validators.DataRequired()]
    )
    submit = wtf.SubmitField('submit')
