from flask import Flask, jsonify, render_template, url_for, request, session, redirect
from myapp import app, mongo
import datetime
from auth import getUser, isLogged
from retrieve_tweets.filters import filter
from retrieve_tweets.tweets_collection import delete_many_tweets, retrieve_all_tweets_text, retrieve_tweet_dates, retrieve_tweets_by_date
import json


@app.route('/delete-all-tweets')
def deleted():
    delete_many_tweets()
    return render_template('index.html')


@app.route('/result-wordcloud/<start_date>/<stop_date>')
def get_little_wordcloud(start_date,stop_date):
    words = retrieve_tweets_by_date(start_date, stop_date)
    return json.dumps(words);


@app.route('/test/<keywords>')
def test(keywords):
    filter(keywords=keywords)
    freq_per_date = retrieve_tweet_dates()
    return render_template('result_wordcloud.html', keywords=keywords, freq_per_date=freq_per_date)

@app.route('/result-wordcloud/')
def wordcloud():
    words = retrieve_all_tweets_text()
    return json.dumps(words)

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
            return redirect(url_for('test', keywords=request.form['keywords']))


def getSessionById(id):
    return mongo.db.sessions.find_one(id)