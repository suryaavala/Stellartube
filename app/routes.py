from flask import Flask, render_template, redirect, request, url_for, abort, flash
from flask_login import LoginManager, login_user, logout_user, login_required
from app import app
from .forms import SignInForm, SignUpForm
from .login_manager import User
from app import database as db

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
        
        if not db.sql_CheckUserExist(username):
            flash('Wrong credentials')
        else:
            print(db.sql_GetPasswordByUsername(username))
            if password == db.sql_GetPasswordByUsername(username)[0][0]:
                user = User(str(db.sql_GetUserIDByUsername(username)))
                login_user(user)
                flash('Successfully logged in')

                next = request.args.get('next')
                #if not is_safe_url(next):
                #    return abort(400)

                return redirect(next or url_for('index'))

    return render_template('sign_in.html', form=signinform)

@app.route('/signup', methods=['get', 'post'])
def signup():
    signupform = SignUpForm()

    if signupform.validate_on_submit():
        username = signupform.username.data
        password = signupform.password.data
        address = signupform.address.data

        if db.sql_CheckUserExist(username):
            flash("Username already exists")
        else:
            if db.sql_InsertUserInfo(username, password, address, 0):
                user = User(str(db.sql_GetUserIDByUsername(username)))
                login_user(user)
                flash('User successful created and logged in')

                next = request.args.get('next')
                return redirect(next or url_for('index'))

    return render_template('sign_up.html', form=signupform)


@app.route('/logout', methods=['get', 'post'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))
