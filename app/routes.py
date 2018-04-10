from flask import Flask, render_template, redirect, request, url_for, abort, flash
from flask_login import LoginManager, login_user, logout_user, login_required
from app import app
from .forms import SignInForm
from .login_manager import User
from .database import sql_StartSQLConnection, sql_Select

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'

@lm.user_loader
def load_user(userid):
    return User(userid)

@app.route('/', methods=['get', 'post'])
def index():
    return render_template('index.html')

@app.route('/signin', methods=['get', 'post'])
def signin():
    signinform = SignInForm()

    # Check sign in attempt
    if signinform.validate_on_submit():
        username = signinform.username.data
        password = signinform.password.data

        conn = sql_StartSQLConnection('localhost', 'admin', 'password', 'blockheads_db')
        count, results = sql_Select(conn, 'select UserID, Username, Passwords from Table_UserInfo where Username="{}"'.format(username))
        
        if count == 0:
            flash('Wrong credentials')
        elif count == 1:
            credentials = results[0]
            if password == credentials[2]:
                user = User(str(credentials[0]))
                login_user(user)
                flash('Successfully logged in')

                next = request.args.get('next')
                #if not is_safe_url(next):
                #    return abort(400)

                return redirect(next or url_for('index'))

    return render_template('sign_in.html', form=signinform)

@app.route('/logout', methods=['get', 'post'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))
