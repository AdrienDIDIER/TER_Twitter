from myapp import mongo, app
import json, bson
import re, collections

from flask import session, jsonify


from flask import session
from stop_words import get_stop_words
import datetime, pytz, time


def stock_tweets(tweet):
    tweets_table = mongo.db.tweets
    tweets_table.insert({'session_id': session['last_session'], 'tweet_object': tweet. _json})


def delete_many_tweets(key=None, value=None):
    tweets_table = mongo.db.tweets
    if key is not None and value is not None:
        results = tweets_table.delete_many({key: value})
    else:
        results = tweets_table.delete_many({})  # Delete all from the collection
    print(results.deleted_count)


def tweets_by_session_id(session_id):
    return mongo.db.tweets.find({'session_id': session_id})


def count_number_of_tweets(session_id):
    return tweets_by_session_id(session_id).count()


def retrieve_all_tweets_text():
    tweets_table = tweets_by_session_id(session['last_session'])
    buffer = []
    for tweet in tweets_table:
        buffer.append(tweet['tweet_object'])
    tweet_text = ""
    for tweet in buffer:
        tweet_text = tweet_text + " " + tweet['full_text']
    return word_splitter(tweet_text)


def word_splitter(tweet_text):
    tweet_text = re.sub(r'[^\w\s]', '', tweet_text)
    tweet_text = re.sub(r'\s\s+', ' ', tweet_text)
    pattern = re.compile('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    pattern.sub('', tweet_text)
    words = tweet_text.split(" ")
    new_words = []
    stop_words = get_stop_words('fr') + get_stop_words('en')
    # print(stop_words)
    for word in words:
        if word.lower() in stop_words or 'RT' in word.lower():
            words.remove(word)
    word_counter = collections.Counter(words)
    for word in word_counter:
        if word_counter[word] >= 3:
            new_words.append({'text': word, 'size': word_counter[word]})
    return new_words

def retrieve_tweet_dates():
    tweets_table = mongo.db.tweets()
    buffer = []
    for tweet in tweets_table.find():
        buffer.append(tweet['tweet_object'])
    date_buffer = []
    for tweet in buffer:
        date_buffer.append(tweet['created_at'])
    return date_to_int(date_buffer)

def date_to_int(tweet_dates):
    buffer = []
    for date in tweet_dates:
        d = datetime.datetime.strptime(date, '%a %b %d %H:%M:%S +0000 %Y').replace(tzinfo=pytz.UTC)
        buffer.append(time.mktime(d.timetuple()))
    print(buffer)
    start_date = int(min(buffer))
    stop_date = int(max(buffer))
    freq = [0]*len(buffer)
    index = 0
    for x in range(start_date,stop_date,10):
        for i in range(len(buffer)):
            if buffer[i] >= float(x) and buffer[i] <= float(x+10):
                freq[index] = freq[index] + 1
        index = index + 1
    new_freq = []
    for x, i in zip(range(start_date, stop_date,11), freq):
        new_freq.append({'freq': i, 'start_date': x, 'stop_date': x+10})
    print(new_freq)
    return new_freq

def retrieve_tweets_by_date(start,stop):
    tweets_table = mongo.db.tweets
    buffer = []
    buffer.append(time.mktime(d.timetuple()))
    for tweet in tweets_table.find():
        buffer.append(tweet['tweet_object'])
    tweet_text = ""
    for tweet in buffer:
        d = datetime.datetime.strptime(tweet['created_at'], '%a %b %d %H:%M:%S +0000 %Y').replace(tzinfo=pytz.UTC)
        if d >= start and d <= stop:
            tweet_text = tweet_text + " " + tweet["full_text"]
    return word_splitter(tweet_text)