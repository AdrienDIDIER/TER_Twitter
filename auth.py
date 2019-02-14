from flask import Flask, render_template, url_for, request, session, redirect
from myapp import app, mongo
from bin.crypto import *
import tweepy
import bcrypt
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

#declaration API Keys

consumer_key = "DT4qrp9j1ttwfsoXWtbhYlwOl"
consumer_secret = "g8X2I3cTbqv5A44zuz5UWa2s7nRUXPfWWRZpUwWOGSahy3tIoU"
access_token = "955782108341063680-0WOfWNVnHv1uXBOpl2Gp3KDgS6HgHSk"
access_token_secret = "CY8bhHMS2sBeript7PjVo2Zw0azfvwwNnmo1GVutOXHSk"
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one({'email': request.form['email']})
        if existing_user is None:
            password = request.form['password']
            consumer_k = request.form['consumer_key']
            consumer_s = request.form['consumer_secret']
            access_t = request.form['access_token']
            access_t_s = request.form['access_token_secret']
            # setting new API Auth
            try:
                api_auth(consumer_k, consumer_s,
                         access_t, access_t_s)
            except tweepy.error.TweepError:
                return render_template('register.html', error=True)

            #crypt password and API parameters
            hash_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            hash_consumer_key = public_key.encrypt(
                consumer_k.encode('utf-8'),
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
            hash_consumer_secret = public_key.encrypt(
                consumer_s.encode('utf-8'),
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
            hash_access_token = public_key.encrypt(
                access_t.encode('utf-8'),
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
            hash_access_token_secret = public_key.encrypt(
                access_t_s.encode('utf-8'),
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
            #inserting user in the database
            users.insert_one({'first_name': request.form['first_name'], 'last_name': request.form['last_name'],
                              'email': request.form['email'], 'password': hash_password,
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
                # decrypt API keys
                consumer_k = private_key.decrypt(
                    login_user['consumer_key'],
                    padding.OAEP(
                        mgf=padding.MGF1(algorithm=hashes.SHA256()),
                        algorithm=hashes.SHA256(),
                        label=None
                    )
                ).decode('utf_8')
                consumer_s = private_key.decrypt(
                    login_user['consumer_secret'],
                    padding.OAEP(
                        mgf=padding.MGF1(algorithm=hashes.SHA256()),
                        algorithm=hashes.SHA256(),
                        label=None
                    )
                ).decode('utf_8')
                access_t = private_key.decrypt(
                    login_user['access_token'],
                    padding.OAEP(
                        mgf=padding.MGF1(algorithm=hashes.SHA256()),
                        algorithm=hashes.SHA256(),
                        label=None
                    )
                ).decode('utf_8')
                access_t_s = private_key.decrypt(
                    login_user['access_token_secret'],
                    padding.OAEP(
                        mgf=padding.MGF1(algorithm=hashes.SHA256()),
                        algorithm=hashes.SHA256(),
                        label=None
                    )
                ).decode('utf_8')
                try:
                    api_auth(consumer_k, consumer_s,
                             access_t, access_t_s)
                    return redirect(url_for('index'))
                except tweepy.error.TweepError:
                    return 'Invalid Api Authentication'
            else:
                return 'Invalid email/password combination'

        else:
            return 'Invalid email/password combination'
    else:
        return render_template('login.html')


def api_auth(consumer_k, consumer_s, access_t, access_t_s):
    global api, auth, consumer_key, consumer_secret, access_token, access_token_secret
    consumer_key = consumer_k
    consumer_secret = consumer_s
    access_token = access_t
    access_token_secret = access_t_s
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    public_tweets = api.home_timeline()
    for tweets in public_tweets:
        print(tweets.text)

@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('index'))


def isLogged():
    return 'email' in session


def getUser():
    if isLogged():
        return mongo.db.users.find_one({'email': session['email']})

def getUserByObjectId(object_id):
    return mongo.db.users.find_one(object_id)

