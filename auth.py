from flask import Flask, render_template, url_for, request, session, redirect
from myapp import app, mongo
import bcrypt
from tweepy_auth import *


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one({'email': request.form['email']})
        if existing_user is None:
            #setting new API Auth
            try:
                changeAPIAuth(request.form['consumer_key'],request.form['consumer_secret'],request.form['access_token'],request.form['access_token_secret'])
            except tweepy.error.TweepError:
                return render_template('register.html', error=True)
            #hashing password and API parameters
            hashpass = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
            hash_consumer_key = bcrypt.hashpw(consumer_key.encode('utf-8'), bcrypt.gensalt())
            hash_consumer_secret = bcrypt.hashpw(consumer_secret.encode('utf-8'), bcrypt.gensalt())
            hash_access_token = bcrypt.hashpw(access_token.encode('utf-8'), bcrypt.gensalt())
            hash_access_token_secret = bcrypt.hashpw(access_token_secret.encode('utf-8'), bcrypt.gensalt())
            #inserting user in the database
            users.insert_one({'first_name': request.form['first_name'], 'last_name': request.form['last_name'],
                              'email': request.form['email'], 'password': hashpass,
                              'consumer_key': hash_consumer_key,
                              'consumer_secret': hash_consumer_secret,
                              'access_token': hash_access_token,
                              'access_token_secret': hash_access_token_secret
                              })
            session['email'] = request.form['email']
            return redirect(url_for('index'))
        else:
            return 'That username already exists!'
    else:
        return render_template('register.html')



@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        users = mongo.db.users
        login_user = users.find_one({'email': request.form['email']})

        if login_user:
            if bcrypt.checkpw(request.form['password'].encode('utf-8'), login_user['password']):
                session['email'] = request.form['email']
                return redirect(url_for('index'))
            else:
                return 'Invalid email/password combination'

        else:
            return 'Invalid email/password combination'
    else:
        return render_template('login.html')


def changeAPIAuth(consumer_key,consumer_secret,access_token,access_token_secret):
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    # Test if authenfication worked, else return tweepy.error.TweepError
    print(api.me())


@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('index'))


def isLogged():
    return 'email' in session


def getUser():
    if isLogged():
        return mongo.db.users.find_one({'email': session['email']})
