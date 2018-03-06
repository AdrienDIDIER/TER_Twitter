from flask import Flask,jsonify, render_template, url_for, request, session, redirect
from myapp import app, mongo
import datetime
from auth import getUser, isLogged
from retrieve_tweets.filters import filter

@app.route('/session/add/', methods=['POST', 'GET'])
@app.route('/session/add/<mode>', methods=['POST', 'GET'])
def addSession(mode=None):
    if request.method == 'GET':
        return render_template('session_create_form.html', mode=mode)
    elif request.method == 'POST':
        if isLogged():
            session_collection = mongo.db.sessions
            user_logged = getUser()
            dateOfDay = datetime.datetime.now()
            documentInserted = session_collection.insert({'user_id': user_logged['_id'], 'session_name': request.form['session_name'],
                                       'start_date': dateOfDay.strftime("%d-%m-%y-%H-%M-%S")})

            session['last_session'] = str(getSessionById(documentInserted)['_id'])
            if request.form['mode'] == 'stream':
                filter(request.form['keywords'], None, True)
            elif request.form['mode'] == 'dated_tweets':
                filter(request.form['keywords'])
            return "<h1>Session created</h1>"

def getSessionById(id):
    return mongo.db.sessions.find_one(id)