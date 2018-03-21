from tweepy_auth import *
from retrieve_tweets.tweets_collection import *
from myapp import app

class Stream(tweepy.StreamListener):
    def on_status(self, status):
        with app.app_context():
            # stock_tweets(status)
            print(status)

def filter(keywords = None, geocode = None, stream = False, startdate = None, stopdate = None, user = None, language = None):
    if stream:
        stream = tweepy.Stream(auth = api.auth, listener = Stream())
        if user is not "":
            keywords = keywords + " from:@" + user

        if geocode is "":
            stream.filter(track=[keywords])
        elif keywords is "" and geocode is not "":
            # Passe d'une chaîne de caractère en un tableau de floats (chaque élément séparé d'une virgule)
            stream.filter(locations=[float(s) for s in geocode.split(",")])
    else:
        query = keywords
        if startdate is not None and stopdate is not None:
            query = query + " since:" + startdate + " until:" + stopdate
        if user is not None:
            query = query + " from:@" + user
        for tweet in tweepy.Cursor(api.search, q=query, tweet_mode="extended", geocode=geocode, lang="fr").items(50):
            stock_tweets(tweet)