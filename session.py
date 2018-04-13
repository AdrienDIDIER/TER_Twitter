from flask import Flask, jsonify, render_template, url_for, request, session, redirect, send_file, Response
from myapp import app, mongo
import datetime
from auth import getUser, isLogged, getUserByObjectId
from myapp import app, mongo
from auth import getUser, isLogged
from retrieve_tweets.filters import *
from index import *
from bson import ObjectId, Binary, Code, BSON
from bson.json_util import dumps
import json

@app.route('/delete-all-tweets')
def deleted():
    delete_many_tweets()
    return render_template('index.html')

@app.route('/result-wordcloud/<start_date>/<stop_date>')
def get_little_wordcloud(start_date,stop_date):
    words = retrieve_tweets_by_date(start_date, stop_date)
    return json.dumps(words)

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
                     "%d-%m-%y-%H-%M-%S"), 'mode': request.form['mode'],
                 'params': {
                     'keywords': request.form['keywords'],
                     'geocode': request.form['geocode'],
                     'start_date': request.form['start_date'] if request.form['mode'] == "dated_tweets" else None,
                     'stop_date': request.form['stop_date'] if request.form['mode'] == "dated_tweets" else None,
                     'twitter_user': request.form['twitter_user'],
                     'language': request.form['language']
                 }
                 })  # Insertion du document session dans la collection session

            # Recuperation de l'id de la dernière session créée
            session['last_session'] = str(getSessionByObjectId(documentInserted)['_id'])
            return redirect(url_for('display_session', session_id = documentInserted))

@app.route('/session/<session_id>', methods=['POST', 'GET'])
def display_session(session_id=None):
    current_session = getSessionByObjectId(ObjectId(session_id))
    session['last_session'] = session_id
    if request.method == 'GET':
        return render_template('session_interface.html', current_session=current_session, number_of_tweets = count_number_of_tweets(session_id))
    if request.is_xhr: # Si la route est appelée via Ajax
        keywords = current_session['params']['keywords']
        geocode = current_session['params']['geocode']
        stream = True if current_session['mode'] == "stream" else False
        startdate = current_session['params']['start_date']
        stopdate = current_session['params']['stop_date']
        user = current_session['params']['twitter_user']
        language = current_session['params']['language']
        filter(keywords, geocode, stream, startdate, stopdate, user, language)
        return render_template('session_interface.html', current_session = current_session)

@app.route('/session/close/')
def close_session():
    dateOfDay = datetime.datetime.now()  # Récupère la date d'aujourd'hui
    mongo.db.sessions.update_one({'_id': ObjectId(session['last_session'])}, {'$set': {
        'last_modification_date': dateOfDay.strftime(
            "%d-%m-%y-%H-%M-%S")
    }})
    return redirect(url_for('index'))


@app.route('/session/delete/')
def delete_session():
    result = mongo.db.tweets.delete_many({'session_id': session['last_session']})
    mongo.db.sessions.delete_one({'_id': ObjectId(session['last_session'])})
    return redirect(url_for('index'))


@app.route('/session/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # <input type="file" name="json">
        file = request.files['json']
        # On lit le contenu du fichier et le stock dans une var
        data = json.loads(file.read().decode('utf-8'))
        # la première case du tableau contient le document de la session exportée
        session_document = data[0]
        del session_document['_id']
        imported_tweets = data[1]  # Un tableau de documents tweets
        exporter_user = getUserByObjectId(ObjectId(session_document['user_id']['$oid']))
        user_logged = getUser()
        # On remplace l'user id par celui de l'utilisateur courrant
        session_document['user_id'] = user_logged['_id']
        # On ajoute le nom et prenom de l'utilisateur qui a exporté la session
        session_document['exporter_user'] = exporter_user['first_name'] + exporter_user['last_name']
        mongo.db.sessions.insert_one(session_document)
        session['last_session'] = str(session_document['_id'])
        tweet_collection = mongo.db.tweets.find_one({"session_id": "5acfa7d14f610629981feee1"})
        for tweet in imported_tweets:
            # Lier les tweets importés à notre nouvelle session
            tweet['session_id'] = session['last_session']
            del tweet['_id']
        mongo.db.tweets.insert_many(imported_tweets)
        return redirect(url_for('display_session', session_id=session['last_session']))


@app.route('/session/download')
def download_file():
    # On récupère le document de la session courrante pour le mettre dans le fichier exporté + nommage du fichier
    current_session = getSessionByObjectId(ObjectId(session['last_session']))
    # On récupère tous les tweets liés à la session
    tweets = mongo.db.tweets.find({'session_id': session['last_session']})
    # On dump tout ça, stocké dans une variable sous forme de tableau
    file_data = dumps([current_session, tweets])
    # On retourne le fichier json qui se dl automatiquement
    return Response(file_data, mimetype="text/plain", headers={
        "Content-Disposition": "attachement;filename=" + current_session['session_name'] + ".json"},
                    content_type="application/json")

def getSessionByObjectId(id):
    return mongo.db.sessions.find_one(id)
