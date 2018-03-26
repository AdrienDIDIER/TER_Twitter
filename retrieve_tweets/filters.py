from tweepy_auth import *
from retrieve_tweets.tweets_collection import *
from myapp import app

class Stream(tweepy.StreamListener):
    def on_status(self, status):
        with app.app_context():
            print(status)
            # stock_tweets(tweet)

def filter(keywords = None, geocode = None, stream = False, startdate = None, stopdate = None, user = None,language = None):
    if stream:
        stream = tweepy.Stream(auth = api.auth, listener = Stream())
        if user is not "":
            user = getIdByUser(user)
        if geocode is not "":
            # Passe d'une chaîne de caractère en un tableau de floats (chaque élément séparé d'une virgule)
            geocode = [float(s) for s in geocode.split(",")]
        stream.filter(locations=geocode, track=[keywords], languages=[language], follow=[user])
    else:
        query = keywords
        if startdate is not None and stopdate is not None:
            query = query + " since:" + startdate + " until:" + stopdate
        if user is not None:
            query = query + " from:@" + user
        for tweet in tweepy.Cursor(api.search, q=query, tweet_mode="extended", geocode=geocode, lang="fr").items(50):
            # stock_tweets(tweet)
            print(tweet)

def getIdByUser(userName):
     return api.get_user(userName).id_str