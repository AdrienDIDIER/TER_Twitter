from flask import Flask
from flask_pymongo import PyMongo
import tweepy

app = Flask(__name__)

app.config.from_pyfile('database.py')


mongo = PyMongo(app)

#import your views here
from index import *
from auth import *
from session import *

if __name__ == '__main__':
    app.run(debug=True, threaded=True)