from retrieve_tweets.filters import filter
from retrieve_tweets.tweets_collection import delete_many_tweets, retrieve_all_tweets_text

from flask import Flask, render_template, url_for, request, session, redirect
from auth import isLogged
from myapp import app, mongo


@app.route('/')
def index():
    userLogged = isLogged()
    user = None
    user_sessions = None
    if userLogged:
        users = mongo.db.users
        user = users.find_one({'email': session['email']})
        user_sessions = mongo.db.sessions.find({'user_id' : user['_id']})
    return render_template('index.html', userLogged=userLogged, user=user,user_sessions = user_sessions)


@app.route('/filtered-results')
def filtered():
    filter("Jawad", startdate="2018-02-25", stopdate="2018-02-27")
    return render_template('index.html')


@app.route('/delete-all-tweets')
def deleted():
    delete_many_tweets()
    return render_template('index.html')


@app.route('/result-wordcloud')
def wordcloud():
    words = retrieve_all_tweets_text()
    return render_template('result_wordcloud.html', words=words)