# -*- coding: utf-8 -*-
"""
Created on Tue Apr  4 10:29:03 2023

@author: kyle.welch
"""

from flask import Flask, render_template, request, redirect
import boto3
application = Flask(__name__)
from werkzeug.utils import secure_filename
import key_config as keys

s3 = boto3.client('s3',
                    aws_access_key_id=keys.ACCESS_KEY_ID,
                    aws_secret_access_key= keys.ACCESS_SECRET_KEY
                     )

BUCKET_NAME='csv-autocube-dump'
msg = ""
UPLOAD_FLAG = False

@application.route('/')  
def home():
    global UPLOAD_FLAG
    if UPLOAD_FLAG == True:
        UPLOAD_FLAG = False
        return render_template("home.html",msg = msg)
    return render_template("home.html",msg = "")

@application.route('/upload',methods=['post'])
def upload():
    if request.method == 'POST':
        img = request.files['file']
        if img:
                filename = secure_filename(img.filename)
                img.save(filename)
                s3.upload_file(
                    Bucket = BUCKET_NAME,
                    Filename=filename,
                    Key = filename
                )
                global msg
                global UPLOAD_FLAG
                msg = "Upload Done!"
                UPLOAD_FLAG = True
        return redirect('/')

if __name__ == "__main__":
    application.run(debug=1)
