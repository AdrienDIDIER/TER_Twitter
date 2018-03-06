from auth import isLogged
from retrieve_tweets.filters import filter
from retrieve_tweets.tweets_collection import delete_many_tweets
from myapp import app, mongo
from flask import Flask,render_template,url_for,request,session,redirect
from flask import Flask, render_template, url_for, request, session, redirect
from auth import isLogged
from myapp import app, mongo

@app.route('/')
def index():
    userLogged = isLogged()
    user = None
    if userLogged:
        users = mongo.db.users
        user = users.find_one({'email': session['email']})
    return render_template('index.html', userLogged=userLogged, user=user)
    userLogged = isLogged()
    user = None
    if userLogged:
        users = mongo.db.users
        user = users.find_one({'email': session['email']})
    return render_template('index.html', userLogged=userLogged, user=user)

@app.route('/filtered-results')
def filtered():
    filter("Nutella")
    return render_template('index.html')

@app.route('/delete-all-tweets')
def deleted():
    delete_many_tweets()
    return render_template('index.html')

