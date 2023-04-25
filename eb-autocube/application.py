# -*- coding: utf-8 -*-
"""
Created on Tue Apr  4 10:29:03 2023

@author: kyle.welch
"""

from flask import Flask, render_template, request, redirect
import boto3
from werkzeug.utils import secure_filename
import key_config as keys
import pandas as pd
from io import StringIO

application = Flask(__name__)

s3 = boto3.client('s3',
                  aws_access_key_id=keys.ACCESS_KEY_ID,
                  aws_secret_access_key=keys.ACCESS_SECRET_KEY
                  )

BUCKET_NAME = 'csv-autocube-dump'
msg = ""
UPLOAD_FLAG = False


@application.route('/')
@application.route('/home')
def home():
    global UPLOAD_FLAG
    if UPLOAD_FLAG:
        UPLOAD_FLAG = False
        return render_template("home.html", msg=msg)
    return render_template("home.html", msg="")


@application.route('/upload', methods=['post', 'get'])
def upload():
    if request.method == 'POST':
        cube = request.files['file']
        
        if cube:
            filename = secure_filename(cube.filename)
            cube.save(filename)
                
            s3.upload_file(
                Bucket=BUCKET_NAME,
                Filename=filename,
                Key=filename
            )

            new_csv = s3.get_object(
                Bucket=BUCKET_NAME,
                Key=filename
                )

            headers = new_csv['Body']
            csv_string = headers.read().decode('utf-8')
            data_full = pd.read_csv(StringIO(csv_string))
            data_top = list(data_full.columns)

            global msg
            global UPLOAD_FLAG
            msg = data_top
            UPLOAD_FLAG = True
        return render_template("select_columns_3.html", msg=data_top)
    return redirect('/')


@application.route('/submit-form', methods=['post', 'get'])
def submit_form():
    column_headers = request.form
    return render_template("home.html", msg=column_headers)


if __name__ == "__main__":
    application.run(debug=True)
