from myapp import mongo, app
import json, bson
import re, collections
from flask import session


def stock_tweets(tweet):
    tweets_table = mongo.db.tweets
    tweet = bson.BSON.encode(json.loads(json.dumps(tweet._json)))
    tweets_table.insert_one({"session_id": session['last_session'] , "tweet_object":tweet}).inserted_id

def delete_many_tweets(key = None, value = None):
    tweets_table = mongo.db.tweets
    if key is not None and value is not None:
        results = tweets_table.delete_many({key: value})
    else:
        results = tweets_table.delete_many({})# Delete all from the collection
    print(results.deleted_count)

def tweets_by_session_id(session_id):
    return mongo.db.tweets.find({'session_id': session_id})

def count_number_of_tweets(session_id):
    return tweets_by_session_id(session_id).count()

def retrieve_all_tweets_text():
    tweets_table = mongo.db.tweets
    buffer = []
    for tweet in tweets_table.find():
        buffer.append(bson.BSON.decode(tweet['tweet_object']))
    tweet_text = ""
    for tweet in buffer:
        tweet_text = tweet_text + " " + tweet["full_text"]
    return word_splitter(tweet_text)


def word_splitter(tweet_text):
    tweet_text = re.sub(r'[^\w\s]', '', tweet_text)
    tweet_text = re.sub(r'\s\s+', ' ', tweet_text)
    words = tweet_text.split(" ")
    new_words = []
    word_counter = collections.Counter(words)
    for word in word_counter:
        new_words.append({'text': word, 'size': word_counter[word]})
    return new_words
