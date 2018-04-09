from flask import Flask, render_template, redirect, request, url_for, abort
from app import app
from .forms import SignInForm
from .login_manager import User


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

        if username == password:
            user = User(username)
            login_user(user)

            next = request.args.get('next')
            #if not is_safe_url(next):
            #    return abort(400)

            return redirect(next or url_for('index'))

    return render_template('sign_in.html', form=signinform)
