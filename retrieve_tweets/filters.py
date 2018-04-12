from tweepy_auth import *
from retrieve_tweets.tweets_collection import *
from myapp import app

class Stream(tweepy.StreamListener):
    def on_status(self, status):
        with app.app_context():
            stock_tweets(status)

def filter(keywords = None, geocode = None, stream = False, startdate = None, stopdate = None, user = None):
    if stream:
        stream = tweepy.Stream(auth = api.auth, listener = Stream())
        # stream.filter(track=[keywords], geocode=[])
        stream.filter(track=[keywords], async = True)
    else:
        query = keywords
        if startdate is not None and stopdate is not None:
            query = query + " since:" + startdate + " until:" + stopdate
        if user is not None:
            query = query + " from:@" + user
        for tweet in tweepy.Cursor(api.search, q=query, tweet_mode="extended", geocode=geocode, lang="fr").items(300):
            stock_tweets(tweet)
        print("Stockage fini")