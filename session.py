from flask import Flask, jsonify, render_template, url_for, request, session, redirect
from myapp import app, mongo
import datetime
from auth import getUser, isLogged
from retrieve_tweets.filters import *
from index import *
from bson import ObjectId


@app.route('/session/add/', methods=['POST', 'GET'])
@app.route('/session/add/<mode>', methods=['POST', 'GET'])
def addSession(mode=None):
    if request.method == 'GET':  # Affichage de la page HTML
        return render_template('session_create_form.html', mode=mode)
    elif request.method == 'POST':  # Envoi de formulaire
        if isLogged():  # Vérificaiton qu'un user est connecté
            session_collection = mongo.db.sessions
            user_logged = getUser()
            dateOfDay = datetime.datetime.now()  # Récupère la date d'aujourd'hui
            documentInserted = session_collection.insert(
                {'user_id': user_logged['_id'], 'session_name': request.form['session_name'],
                 'start_date': dateOfDay.strftime(
                     "%d-%m-%y-%H-%M-%S"), 'mode': request.form['mode'],
                 'params': {
                     'keywords': request.form['keywords'],
                     'geocode': request.form['geocode'],
                     'start_date': request.form['start_date'] if request.form['mode'] is 'dated_tweets' else None,
                     'stop_date': request.form['stop_date'] if request.form['mode'] is 'dated_tweets' else None,
                     'twitter_user': request.form['twitter_user'],
                     'language': request.form['language']
                 }
                 })  # Insertion du document session dans la collection session

            # Recuperation de l'id de la dernière session créée

            session['last_session'] = str(getSessionByObjectId(documentInserted)['_id'])
            if request.form['mode'] == 'stream':
                return redirect(url_for('display_session', session_id=documentInserted))
            elif request.form['mode'] == 'dated_tweets':
                filter(request.form['keywords'],
                       user=request.form['twitter_user'],
                       startdate=request.form['start_date'],
                       stopdate=request.form['stop_date'])
            return wordcloud()


@app.route('/session/<session_id>', methods=['POST', 'GET'])
def display_session(session_id=None):
    current_session = getSessionByObjectId(ObjectId(session_id))
    if request.method == 'GET':
        return render_template('session_interface.html', current_session=current_session)
    if request.is_xhr: # Si la route est appelée via Ajax
        if current_session['mode'] == "stream":
            filter(current_session['params']['keywords'], current_session['params']['geocode'], True, None, None,
                   current_session['params']['twitter_user'], current_session['params']['language'])
            return render_template('session_interface.html', current_session=current_session)

def getSessionByObjectId(id):
    return mongo.db.sessions.find_one(id)
