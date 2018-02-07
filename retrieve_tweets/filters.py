from tweepy_auth import *
from retrieve_tweets.tweets_collection import *

class Stream(tweepy.StreamListener):
    def on_status(self, status):
        stock_tweets(status)

def filter(keywords = None, geocode = None, stream = False):
    if stream:
        stream = tweepy.Stream(auth=api.auth, listener=Stream())
        stream.filter(track=[keywords], geocode=[])
    else:
        for tweet in tweepy.Cursor(api.search, q=keywords, geocode=geocode).items(50):
            stock_tweets(tweet)