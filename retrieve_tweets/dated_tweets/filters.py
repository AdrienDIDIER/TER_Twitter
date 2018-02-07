from tweepy_auth import *
from retrieve_tweets.tweets_collection import *

def filter(keywords = None, geocode = None):
    for tweet in tweepy.Cursor(api.search, q = keywords, geocode=geocode).items(50):
        stock_tweets(tweet)
