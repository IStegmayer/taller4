from rcity import app

import os
from flask import flash, request, redirect, url_for, session
from werkzeug.utils import secure_filename
from flask_cors import CORS, cross_origin
import logging

@app.route('/upload', methods=['POST'])
@cross_origin()
def fileUpload():
    print(request.form)
    target=os.path.join(app.config['UPLOAD_FOLDER'])
    if not os.path.isdir(target):
        os.mkdir(target)
    file = request.files['file'] 
    filename = secure_filename(file.filename)
    destination="/".join([target, filename])
    file.save(destination)
    session['uploadFilePath']=destination
    response="Whatever you wish too return"
    return response