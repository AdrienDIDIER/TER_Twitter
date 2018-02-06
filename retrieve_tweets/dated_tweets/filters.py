from tweepy import api
from retrieve_tweets.tweets_collection import *

def filter(keywords = None, user_screen_name = None, geocode = None):

    for tweet in api.Cursor(api.search, keyword = keywords + " " + user_screen_name, geocode=geocode):
        stock_tweets(tweet)
