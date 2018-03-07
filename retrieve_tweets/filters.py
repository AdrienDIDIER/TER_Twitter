from tweepy_auth import *
from retrieve_tweets.tweets_collection import *
from myapp import app

class Stream(tweepy.StreamListener):
    def on_status(self, status):
        with app.app_context():
            stock_tweets(status)

def filter(keywords = None, geocode = None, stream = False, startdate = None, stopdate = None):
    if stream:
        stream = tweepy.Stream(auth = api.auth, listener = Stream())
        # stream.filter(track=[keywords], geocode=[])
        stream.filter(track=[keywords], async = True)
    else:
        query = keywords + " since:" + startdate + " until:" + stopdate
        for tweet in tweepy.Cursor(api.search, q=query, tweet_mode = "extended", geocode=geocode, lang="fr").items(50):
            stock_tweets(tweet)