from flask import Flask
from flask_pymongo import PyMongo

app = Flask(__name__)

app.config.from_pyfile('database.py')
app.config['MONGO_URI'] = 'mongodb://tweetostats:tweetostats34@ds125288.mlab.com:25288/tweetostats_db'

mongo = PyMongo(app)

#import your views here
from index import *
from auth import *
from session import *

if __name__ == '__main__':
    app.run(debug=True, threaded=True)