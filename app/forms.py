from flask_wtf import FlaskForm
import wtforms as wtf
import flask_wtf.file as fwtff

class SignInForm(FlaskForm):
    email = wtf.StringField(
        'email',
        validators=[wtf.validators.DataRequired()]
    )
    password = wtf.PasswordField(
        'password',
        validators=[wtf.validators.DataRequired()]
    )
    remember_me = wtf.BooleanField('remember me')
    submit = wtf.SubmitField('submit')

class SignUpForm(FlaskForm):
    first_name = wtf.StringField(
        'fname',
        validators=[wtf.validators.DataRequired()]
    )
    last_name = wtf.StringField(
        'lname',
        validators=[wtf.validators.DataRequired()]
    )
    email = wtf.StringField(
        'email',
        validators=[wtf.validators.DataRequired()]
    )
    password = wtf.PasswordField(
        'password', 
        validators=[wtf.validators.DataRequired()]
    )
    confirm_password = wtf.PasswordField(
        'confirm password',
        validators=[wtf.validators.DataRequired()]
    )
    submit = wtf.SubmitField('submit')

class UploadVideoForm(FlaskForm):
    title = wtf.StringField(
        'title',
        validators=[wtf.validators.DataRequired()]
    )
    description = wtf.TextAreaField(
        'description',
        validators=[wtf.validators.DataRequired()]
    )
    price = wtf.DecimalField(
        'price',
        validators=[wtf.validators.DataRequired()]
    )
    labels = wtf.StringField(
        'labels',
        validators=[wtf.validators.DataRequired()]
    )
    video_file = fwtff.FileField(
        'vfile',
        validators=[
            fwtff.FileRequired(),
            fwtff.FileAllowed(['mp4'])
        ]
    )
    submit = wtf.SubmitField('submit')
