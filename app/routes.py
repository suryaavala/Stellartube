from flask import Flask, make_response, render_template, redirect, request, url_for, abort, flash, send_from_directory, jsonify
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
from app.asset import *

import json
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
# Page allows users to sign into their account
@app.route('/signin', methods=['get', 'post'])
def signin():
    # Redirect to index page if user already logged in
    if fl.current_user.is_authenticated:
        return redirect(url_for('index'))

    signinform = frm.SignInForm()

    # Errors
    error_unf = False # Error: User not found

    # Check sign in attempt
    if signinform.validate_on_submit():
        email = signinform.email.data
        password = signinform.password.data
        uid = db.sql_doesUserExist(email)

        if not uid:
            error_unf = True
        else:
            if db.sql_checkUserPassword(uid, password):
                user = lm.User(str(uid))
                fl.login_user(user)
                flash('Successfully logged in')

                next = request.args.get('next')

                return redirect(next or url_for('index'))

    return render_template('sign_in.html', form=signinform, error_unf=error_unf)


# Sign Up Page
# Page allows users to create an account
@app.route('/signup', methods=['get', 'post'])
def signup():
    # Redirect to index page if user already logged in
    if fl.current_user.is_authenticated:
        return redirect(url_for('index'))

    signupform = frm.SignUpForm()

    # Errors
    error_uae = False # Error: User already exists
    error_pnv = False # Error: Password not valid
    error_pdm = False # Error: Passwords dont match

    if signupform.validate_on_submit():
        fname = signupform.first_name.data
        lname = signupform.last_name.data
        email = signupform.email.data
        password = signupform.password.data
        cpassword = signupform.confirm_password.data

        # Validate data
        if db.sql_doesUserExist(email):
            error_uae = True
        if not validPassword(password):
            error_pnv = True
        if not cpassword == password:
            error_pdm = True
        
        if not (error_uae or error_pnv or error_pdm):
            # Blockchain user creation
            user_on_blockchain = Stellar_block()
            user_on_blockchain.create_account()
            passphrase = user_on_blockchain.get_passphrase()
            balance = float(user_on_blockchain._get_balance())
            
            # Add user to database
            if not db.sql_addUser(email, password, fname, lname, passphrase, balance):
                user = lm.User(str(db.sql_doesUserExist(email)))
                fl.login_user(user)
                next = request.args.get('next')
                return redirect(next or url_for('index'))

    return render_template('sign_up.html', form=signupform,
        error_uae=error_uae, error_pnv=error_pnv, error_pdm=error_pdm)


# Video Page
# Page for relevent video. Allows playback and download of video if the current
# user owns or purchased it, or the video is free. Links to purchase page if
# not owned and not purchased to current user
@app.route('/watch/<int:video_id>', methods=['get', 'post'])
def watch_video(video_id):
 
    user_purchases = []
    videoIsPurchased = False

    if fl.current_user.is_authenticated:
        user_passphrase = db.sql_getAllUserInfo(fl.current_user.id)[3]
        user = Stellar_block(user_passphrase)

        if user._get_transactions():
            user_purchases = [int(t[1].split('bought')[1]) for t in user._get_transactions()]
            if video_id in user_purchases:
                videoIsPurchased = True

    if request.method == "POST":
        if  "confirm_buy" in request.form:
            buy_content(video_id)
            return redirect(url_for('watch_video', video_id=video_id))

    video = db.sql_getVideo(video_id)
    
    return render_template(
        'view_video.html',
        video_id=video_id,
        video_owner=db.sql_getUser(video[0])[0],
        video_title=video[2],
        video_desc=video[3],
        video_path=url_for('static', filename='videos/%s'%video[5]) if videoIsPurchased else "",
        video_price = video[4],
        video_thumbnail=url_for('static', filename='images/blockmart_logo.svg'),
        videoIsPublic=True if float(video[4]) == 0 else False,
        videoIsOwned=True if fl.current_user.is_authenticated and 
            str(fl.current_user.id) == str(video[0]) else False,
        videoIsPurchased=videoIsPurchased)


# Logout Page
# Logs user out of account then redirects to index page
@app.route('/logout', methods=['get', 'post'])
@fl.login_required
def logout():
    fl.logout_user()
    return redirect(url_for('index'))


# Video Upload Page
# Page for uploading videos
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
        hasUploaded = db.sql_addVideo(int(fl.current_user.id), vtitle, vdescription,vprice, vfilename, vlabels)

        if not hasUploaded:
            return redirect(url_for('index'))

    return render_template('upload_video.html', form=uploadform)


# Download Page
# Serves video file to user for download
@app.route('/download/<int:video_id>', methods=['get', 'post'])
def download(video_id):
    # check if page request is from the relevent video page else redirect to
    # the video page
    if request.referrer and request.referrer.endswith(
            url_for('watch_video', video_id=video_id)):

        video = db.sql_getVideo(video_id)
        if video:
            vfilename = video[5]
            vdir = os.path.join(app.root_path, 'static/videos')
            return send_from_directory(directory=vdir,
                filename=vfilename, as_attachment=True)
        else:
            return redirect(url_for('index'))

    return redirect(url_for('watch_video', video_id=video_id))


# Search Page
# Displays results of search query
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


# Statistics Page
@app.route('/statistic', methods=['get', "POST"])
def statistic():
    date = {}
    labels = []
    values = []
    a = 0
    for userid in db.sql_getAllUserID():
        user_passphare = db.sql_getAllUserInfo(userid[0])[3]
        user = Stellar_block(user_passphare)
        for time in user._get_transactions():
            d = str(time[0].split('T')[0])
            if not date.has_key(d):
                date[d] = 1
            else:
                date[d] += 1
    items = date.items()
    items.sort()
    print(items)
    for label, value in items:
        labels.append(label)
        values.append(value)
    if request.method =="GET":
        return render_template('statistic.html', labels=labels, values=values)
    else:
        return jsonify(labels=labels, values = values)


# User Library Page
# Displays content owned and purchased by current user
@app.route('/mylibrary', methods=['get', 'post'])
@fl.login_required
def user_library():
    user_passphrase = db.sql_getAllUserInfo(fl.current_user.id)[3]
    user = Stellar_block(user_passphrase)

    uploads_v_ids = db.sql_getUserVideos(fl.current_user.id)
    video_uploads = getVideosFromList(uploads_v_ids)

    purchases_v_ids = []    

    ut = user._get_transactions()
    print(ut)
    if ut:
        for t in user._get_transactions():
            trans = int(t[1].split('bought')[1])
            if not trans in uploads_v_ids:
                purchases_v_ids += [trans]
    video_purchases = getVideosFromList(purchases_v_ids)
    return render_template('user_library.html', video_uploads=video_uploads,
        video_purchases=video_purchases)


# Helper Functions

def validPassword(pw):
    return True if len(pw) > 7 and len(pw) < 33 else False

def buy_content(video_id):
    vid = db.sql_getVideo(video_id)
    vid_owner = db.sql_getUser(vid[0])

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
        trusting = trust_asset(owner._generate_keypair(), buyer._generate_keypair(), 'Video{}'.format(str(video_id)))
        print('Asset trust:{}'.format(trusting))
        sending_asset = send_asset(owner._generate_keypair(), buyer._generate_keypair(), 'Video{}'.format(str(video_id)))
        print('Sending asset:{}'.format(sending_asset))
        db.sql_editUserBalance(vid[0], owner._get_balance())
        db.sql_editUserBalance(fl.current_user.get_id(), buyer._get_balance())
        return 1
    else:
        print(result)
        return 0


# Function: getVideosFromList(v_ids)
# Takes an array of video IDs and returns a list of videoInfo objects
def getVideosFromList(v_ids):
    videos = []
    for v in v_ids:
        vi = db.sql_getVideo(v)
        videos.append(
            mdl.videoInfo(v, int(vi[0]), vi[1], vi[2], vi[3], vi[4],
                'uploads/'+vi[5], url_for('static', filename='images/blockmart_logo.svg'))
	)
    return videos
