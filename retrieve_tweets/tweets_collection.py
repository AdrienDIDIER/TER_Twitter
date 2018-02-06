from database import mongo
import json, bson

def stock_tweets(tweet):
    tweets = mongo.db.tweets
    tweet = bson.BSON.encode(json.loads(json.dumps(tweet._json)))
    tweets.insert({"session_id" : 1, "tweet_object" : tweet}).inserted_id
