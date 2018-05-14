from flask import Flask, render_template, redirect, request, url_for, abort, flash, send_from_directory
from flask import Markup as fm
from app import app
from app import models as mdl
from app import forms as frm
from app import login_manager as lm
from app import database as db
from werkzeug.utils import secure_filename
import flask_login as fl
import os
from app.stellar_block import Stellar_block

import sys
sys.path.append('./app')

# Specify login view for login manager
lm.lm.login_view = 'signin'


# Homepage
# This is the main page of the website. From here users can search for videos,
# login and logout of their account, link to their purchases and uploads, link
# to their account details, link to the upload page, and access the help page
@app.route('/', methods=['get', 'post'])
def index():
    v_ids = list(map(int, db.sql_searchVideos('', 100)))
    videos = getVideosFromList(v_ids)

    return render_template('index.html', videos=videos)

# Sign In Page
# Page allows users to sign into their account if they have one, or go to the
# sign up page, and request their password if they have forgetten it


@app.route('/signin', methods=['get', 'post'])
def signin():
    signinform = frm.SignInForm()

    # Check sign in attempt
    if signinform.validate_on_submit():
        email = signinform.email.data
        password = signinform.password.data
        uid = db.sql_doesUserExist(email)

        if not uid:
            print("Error")
            flash('Wrong credentials')
        else:
            if db.sql_checkUserPassword(uid, password):
                user = lm.User(str(uid))
                fl.login_user(user)
                flash('Successfully logged in')

                next = request.args.get('next')

                return redirect(next or url_for('index'))

    return render_template('sign_in.html', form=signinform)


@app.route('/signup', methods=['get', 'post'])
def signup():
    signupform = frm.SignUpForm()

    if signupform.validate_on_submit():
        fname = signupform.first_name.data
        lname = signupform.last_name.data
        email = signupform.email.data
        password = signupform.password.data
        # NOTE: Blockchain user creation
        user_on_blockchain = Stellar_block()
        user_on_blockchain.create_account()
        passphrase = user_on_blockchain.get_passphrase()
        balance = float(user_on_blockchain._get_balance())

        if db.sql_doesUserExist(email):
            flash("Email already in use")
        else:
            if not db.sql_addUser(email, password, fname, lname, passphrase, balance):
                user = lm.User(str(db.sql_doesUserExist(email)))
                fl.login_user(user)
                flash('User successful created and logged in')

                next = request.args.get('next')
                return redirect(next or url_for('index'))

    return render_template('sign_up.html', form=signupform)


@app.route('/watch/<int:video_id>', methods=['get', 'post'])
def watch_video(video_id):
    video = db.sql_getVideo(video_id)

    return render_template(
        'view_video.html',
        video_id=video_id,
        video_name=video[2],
        video_desc=video[3],
        video_path=url_for('static', filename='videos/%s' % video[5]),
        videoPrice=video[4],
        videoIsPublic=True if float(video[4]) == 0 else False,
        videoIsOwned=True if fl.current_user.is_authenticated and
        str(fl.current_user.id) == str(video[0]) else False,
        videoIsPurchased=False)


@app.route('/logout', methods=['get', 'post'])
@fl.login_required
def logout():
    fl.logout_user()
    return redirect(url_for('index'))


@app.route('/upload', methods=['get', 'post'])
@fl.login_required
def upload():
    uploadform = frm.UploadVideoForm()

    if uploadform.validate_on_submit():
        vtitle = uploadform.title.data
        vdescription = uploadform.description.data
        vprice = uploadform.price.data
        vlabels = uploadform.labels.data
        vfile = uploadform.video_file.data
        vfilename = secure_filename(vfile.filename)
        vfilepath = os.path.join(app.root_path, 'static/videos', vfilename)
        vfile.save(vfilepath)

        hasUploaded = db.sql_addVideo(int(fl.current_user.id), vtitle, vdescription,
                                      vprice, vfilename, vlabels)

        if not hasUploaded:
            return redirect(url_for('index'))

    return render_template('upload_video.html', form=uploadform)


@app.route('/download/<int:video_id>', methods=['get', 'post'])
def download(video_id):
    video = db.sql_getVideo(video_id)
    if video:
        vfilename = video[5]
        vdir = os.path.join(app.root_path, 'static/videos')
        return send_from_directory(directory=vdir, filename=vfilename,
                                   as_attachment=True)
    else:
        return redirect(url_for('index'))


@app.route('/search', methods=['get'])
def search():
    if request.method == 'GET':
        search_query = request.args.get('search_query', None)
        if search_query:
            v_ids = list(map(int, db.sql_searchVideos(search_query, 1000)))
            videos = getVideosFromList(v_ids)

            return render_template('search_results.html', videos=videos,
                                   search_query=search_query)

    return redirect(url_for('index'))


@app.route('/mylibrary', methods=['get', 'post'])
@fl.login_required
def user_library():
    uploads_v_ids = db.sql_getUserVideos(fl.current_user.id)
    video_uploads = getVideosFromList(uploads_v_ids)
    purchases_v_ids = []  # Replace with function that returns list of purchased video IDs
    video_purchases = getVideosFromList(purchases_v_ids)
    return render_template('user_library.html', video_uploads=video_uploads,
                           video_purchases=video_purchases)


# Purchase Confirmation page
#
# Page loaded into an iframe that prompts the user to confirm their
# their purchase
@app.route('/buy/<int:video_id>', methods=['get', 'post'])
@fl.login_required
def buy_content(video_id):
    vid = db.sql_getVideo(video_id)
    vid_owner = db.sql_getUser(vid[0])

    if request.method == "POST":

        if "confirm_buy" in list(request.form.keys()):
            video_price = vid[4]
            owner_passphrase = db.sql_getAllUserInfo(vid[0])[3]
            buyer_passphrase = db.sql_getAllUserInfo(
                fl.current_user.get_id())[3]
            memo = '{}bought{}'.format(fl.current_user.get_id(), video_id)

            owner = Stellar_block(owner_passphrase)
            buyer = Stellar_block(buyer_passphrase)

            result = buyer.transfer(video_price, owner.get_pubkey(), memo)
            if result == 'SUCCESS':
                print('Successfully bought video')
            else:
                print(result)

            db.sql_editUserBalance(vid[0], owner._get_balance())
            db.sql_editUserBalance(
                fl.current_user.get_id(), buyer._get_balance())

        return redirect(url_for("watch_video", video_id=video_id))

    return render_template("transaction_page.html",
                           video_thumbnail=url_for(
                               'static', filename='images/blockmart_logo.svg'),
                           video_title=vid[2],
                           video_owner=vid_owner[0],
                           video_price=vid[4],
                           video_id=video_id)


# Helper Functions

# Function: getVideosFromList(v_ids)
# Takes an array of video IDs and returns a list of videoInfo objects
def getVideosFromList(v_ids):
    videos = []
    for v in v_ids:
        vi = db.sql_getVideo(v)
        videos.append(mdl.videoInfo(v, int(vi[0]),
                                    vi[1], vi[2], vi[3], vi[4], 'uploads/'+vi[5],
                                    url_for('static', filename='images/blockmart_logo.svg'))
                      )

    return videos
