from retrieve_tweets.tweets_collection import *
from myapp import *
from tweepy_auth import *
from retrieve_tweets.tweets_collection import *
from flask import render_template

stream_stop = False  # Variable globale pour permettre le partage de la variable entre les 2 threads.

class Stream(tweepy.StreamListener):
    def on_status(self, status):
        if not stream_stop:
            # print(status)
            stock_tweets(status)
        else:
            return False

def filter(keywords=None, geocode=None, stream=False, startdate=None, stopdate=None, user=None, language=None):
    if geocode is not "":
        # Passe d'une chaîne de caractère en un tableau de floats (chaque élément séparé d'une virgule)
        geocode = [float(s) for s in geocode.split(",")]
    if stream:
        global stream_stop
        stream_stop = False

        if user is not "":
            user = getIdByUser(user)

        stream_o = tweepy.Stream(auth=api.auth, listener=Stream())
        stream_o.filter(locations=geocode, track=[keywords], languages=[language], follow=[user])
    else:
        geocode = None # TODO: FIX (Filtrer par geocode) et fix language
        query = keywords
        if startdate != "" and stopdate != "":
            query = query + " since:" + startdate + " until:" + stopdate
        if user != "":
            query = query + " from:@" + user
            print(language)
        if language == "":
            language = "fr"
        for tweet in tweepy.Cursor(api.search, q=query, tweet_mode="extended", geocode=geocode, language=language).items(200):
            stock_tweets(tweet)
        print("stockage fini")

@app.route('/session/stream/stop')
def stopStream():
    global stream_stop
    stream_stop = True
    return render_template('session_create_form.html')  # On devrait rien retourner (ou page vide) car Ajax

def getIdByUser(userName):
    return api.get_user(userName).id_str
