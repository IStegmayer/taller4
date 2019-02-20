from rcity import app, db

import os
from flask import flash, request, redirect, url_for, session, jsonify, abort
from werkzeug.utils import secure_filename
from flask_cors import CORS, cross_origin
from flask_login import current_user, login_user, logout_user, login_required

from .models import User, Replay
import logging


@app.route('/api/upload', methods=['POST'])
#@login_required
def fileUpload():
    target=os.path.join(app.config['UPLOAD_FOLDER'])
    if not os.path.isdir(target):
        os.mkdir(target)
    file = request.files['file'] 

    if not file.filename.endswith('.replay'):
        return jsonify({'errorMessage': 'Incorrect file extension.'})

    filename = secure_filename(file.filename)


    replay = Replay.query.filter_by(replayFile=filename).first()
    if replay is not None:
        return jsonify({'errorMessage': 'File name already in use.'})

    destination="/".join([target, filename])
    file.save(destination)
    replay = Replay(replayFile=filename,
                    description=request.form['desc'],
                    tag=request.form['toggle'],
                    user_name=request.form['username'])
    db.session.add(replay)
    db.session.commit()

    return jsonify({'msg': 'asdf'}), 201    

@app.route('/api/register', methods=['POST'])
def register():
    try:
        # if current_user.is_authenticated:
            # return redirect(url_for('index'))
        form = request.form
        user = User(username=form['username'], email=form['email'])
        user.set_password(form['pw'])
        db.session.add(user)
        db.session.commit()
        return jsonify({'msg': 'User {} registered successfully.'.format(user.username)}), 201
    except:
        abort(404)

@app.route('/api/validate-register', methods=['POST'])
def validate_register():

    username = User.query.filter_by(username=request.form['username']).first()
    if username is not None:
        return jsonify({'error': 'usernameValidation', 'feedback': 'Username already in use'})

    email = User.query.filter_by(email=request.form['email']).first()
    if email is not None:
        return jsonify({'error': 'emailValidation', 'feedback': 'Email already in use'})

    return jsonify({'msg': 'sabelo'})

@app.route('/api/login', methods=['POST'])
def login():
    try:
        # if current_user.is_authenticated:
        #     return redirect(url_for('home'))
        form = request.form
        
        user = User.query.filter_by(username=form['username']).first()
        if user is None or not user.check_password(form['pw']):
            return jsonify({'error': 'Incorrect username or password'}), 201
        login_user(user)
        return jsonify({'username': current_user.username}), 201
    except:
        abort(404)
    
@app.route('/api/logout', methods=['GET', 'POST'])
# @login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/api/get-replays', methods=['GET'])
def get_replays():
    replays = Replay.query.all()
    rbuffer = [r.serialize for r in replays]
    for r in rbuffer:
        r['liked'] = 'Unlike'
    return jsonify({'msg': 'holo', 'replays': rbuffer}), 201

@app.route('/api/get-user-replays/<user>', methods=['GET'])
def get_user_replays(user):
    from sqlalchemy import func
    replays = Replay.query.filter(func.lower(Replay.user_name) == func.lower(user)).all()
    rbuffer = [r.serialize for r in replays]
    for r in rbuffer:
        r['liked'] = 'Unlike'
    print(rbuffer)
    return jsonify({'msg': 'holo', 'replays': rbuffer}), 201
    

@app.route('/api/userino', methods=['GET', 'POST'])
def userino():
    if current_user.is_authenticated:
        return 'Yes'
    else:
        return 'No'

    return current_user.__repr__()


@app.errorhandler(404)
def page_not_found(e):
    return jsonify(error=404, text="asdf"), 404