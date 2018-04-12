from flask import Flask, render_template, url_for, request, session, redirect
from auth import isLogged
from myapp import app, mongo

@app.route('/')
def index():
    userLogged = isLogged()
    user = None
    user_sessions = None
    sessionAmount = None
    if userLogged:
        users = mongo.db.users
        user = users.find_one({'email': session['email']})
        user_sessions = mongo.db.sessions.find({'user_id': user['_id']})
        sessionAmount = user_sessions.count()
    return render_template('index.html', userLogged=userLogged, user=user, user_sessions=user_sessions,
                           sessionAmount=sessionAmount)