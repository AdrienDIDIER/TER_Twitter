from myapp import app, mongo
from auth import getUser, isLogged
from retrieve_tweets.filters import *
from index import *
from bson import ObjectId

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

@app.route('/session/close/<session_id>')
def close_session(session_id=None):
    current_session = getSessionByObjectId(ObjectId(session_id))
    dateOfDay = datetime.datetime.now()  # Récupère la date d'aujourd'hui
    mongo.db.sessions.update_one({'_id': current_session['_id']}, {'$set': {
        'last_modification_date': dateOfDay.strftime(
                     "%d-%m-%y-%H-%M-%S")
    }})
    return redirect(url_for('index'))

def getSessionByObjectId(id):
    return mongo.db.sessions.find_one(id)
