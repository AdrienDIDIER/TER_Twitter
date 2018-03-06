from myapp import mongo
import json, bson



def stock_tweets(tweet):
    tweets_table = mongo.db.tweets
    tweet = bson.BSON.encode(json.loads(json.dumps(tweet._json)))
    tweets_table.insert_one({"session_id" : 1, "tweet_object" : tweet}).inserted_id

def delete_many_tweets(key = None, value = None):
    tweets_table = mongo.db.tweets
    if key is not None and value is not None:
        results = tweets_table.delete_many({key : value})
    else:
        results = tweets_table.delete_many({})# Delete all from the collection
    print(results.deleted_count)