from flask import Flask, jsonify, render_template, url_for, request, session, redirect
from myapp import app, mongo
import datetime
from auth import getUser, isLogged
from retrieve_tweets.filters import filter
from index import wordcloud


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
                     "%d-%m-%y-%H-%M-%S")})  # Insertion du document session dans la collection session

            # Recuperation de l'id de la dernière session créée
            session['last_session'] = str(getSessionById(documentInserted)['_id'])
            if request.form['mode'] == 'stream':
                filter(request.form['keywords'], None, True)
            elif request.form['mode'] == 'dated_tweets':
                filter(request.form['keywords'],
                       user=request.form['twitter_user'],
                       startdate=request.form['start_date'],
                       stopdate=request.form['stop_date'])
            return wordcloud()

@app.route('/session/<session_id>', methods=['POST', 'GET'])
def display_session(session_id=None):
    render_template('session_interface.html')



def getSessionById(id):
    return mongo.db.sessions.find_one(id)
