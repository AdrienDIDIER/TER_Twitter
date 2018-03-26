from tweepy_auth import *
from retrieve_tweets.tweets_collection import *
from myapp import app
from flask import render_template

class Stream(tweepy.StreamListener):
    def on_status(self, status):
        if not stopStream():
            with app.app_context():
                print(status)
                # stock_tweets(status)
        else:
            return False

def filter(keywords = None, geocode = None, stream = False, startdate = None, stopdate = None, user = None,language = None):
    if stream:
        session['stop_stream'] = False
        stream_o = tweepy.Stream(auth = api.auth, listener = Stream())
        if user is not "":
            user = getIdByUser(user)
        if geocode is not "":
            # Passe d'une chaîne de caractère en un tableau de floats (chaque élément séparé d'une virgule)
            geocode = [float(s) for s in geocode.split(",")]
        stream_o.filter(locations=geocode, track=[keywords], languages=[language], follow=[user])
    else:
        query = keywords
        if startdate is not None and stopdate is not None:
            query = query + " since:" + startdate + " until:" + stopdate
        if user is not None:
            query = query + " from:@" + user
        for tweet in tweepy.Cursor(api.search, q=query, tweet_mode="extended", geocode=geocode, lang="fr").items(50):
            # stock_tweets(tweet)
            print(tweet)

@app.route('/session/add/stream/stop')
def stopStreamRequest():
    session['stop_stream'] = True
    return render_template('session_create_form.html') # On devrait rien retourner (ou page vide) car Ajax

def stopStream():
    if session['stop_stream'] is False:
        return False
    else:
        return True

def getIdByUser(userName):
     return api.get_user(userName).id_str