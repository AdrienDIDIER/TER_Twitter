from flask import Flask, jsonify, render_template, url_for, request, session, redirect, send_file, Response
from myapp import app, mongo
import datetime
from auth import getUser, isLogged, getUserByObjectId
from retrieve_tweets.filters import *
from index import *
from bson import ObjectId, Binary, Code, BSON
from bson.json_util import dumps
import json


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
    session['last_session'] = session_id
    if request.method == 'GET':
        return render_template('session_interface.html', current_session=current_session,
                               number_of_tweets=count_number_of_tweets(session_id))
    if request.is_xhr:  # Si la route est appelée via Ajax
        if current_session['mode'] == "stream":
            filter(current_session['params']['keywords'], current_session['params']['geocode'], True, None, None,
                   current_session['params']['twitter_user'], current_session['params']['language'])
            return render_template('session_interface.html', current_session=current_session)


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
        data = json.loads(file.read())
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
