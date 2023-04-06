# -*- coding: utf-8 -*-
"""
Created on Tue Apr  4 10:29:03 2023

@author: kyle.welch
"""

from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return '<h1> Hello, World! </h1>'

#test!