from myapp import mongo, app
import json, bson
import re, collections

from flask import session, jsonify


from flask import session
from stop_words import get_stop_words
import datetime, pytz, time

def stock_tweets(tweet):
    tweets_table = mongo.db.tweets
    print(tweets_by_session_id(session['last_session']).count())
    if tweets_by_session_id(session['last_session']).count() > 0:
        for tw in tweets_by_session_id(session['last_session']):
            if tweet._json['id_str'] == tw['tweet_object']['id_str']:
                return 0
        tweets_table.insert({'session_id': session['last_session'], 'tweet_object': tweet._json})
        return 1
    else:
        tweets_table.insert({'session_id': session['last_session'], 'tweet_object': tweet._json})
        return 1


def delete_many_tweets(key = None, value = None):
    tweets_table = mongo.db.tweets
    if key is not None and value is not None:
        results = tweets_table.delete_many({key: value})
    else:
        results = tweets_table.delete_many({})# Delete all from the collection

def tweets_by_session_id(session_id):
    return mongo.db.tweets.find({'session_id': session_id})

def count_number_of_tweets(session_id):
    return tweets_by_session_id(session_id).count()

def retrieve_all_tweets_text():
    if 'last_session' in session:
        tweets_table = tweets_by_session_id(session['last_session'])
        tweet_text = ""
        for tweet in tweets_table:
            if 'full_text' in tweet['tweet_object']:
                tweet_text = tweet_text + tweet['tweet_object']['full_text']
            elif 'text' in tweet['tweet_object']:
                tweet_text = tweet_text + tweet['tweet_object']['text']
        return word_splitter(tweet_text)


def word_splitter(tweet_text):
    tweet_text = re.sub(r'[^\w\s]', '', tweet_text)
    tweet_text = re.sub(r'\s\s+', ' ', tweet_text)
    tweet_text = re.sub(r"http\S+", "", tweet_text)
    words = tweet_text.split(" ")
    new_words = []
    stop_words = get_stop_words('fr') + get_stop_words('en')
    words = [word for word in words if word.lower() not in stop_words and 'RT' not in word]
    word_counter = collections.Counter(words)
    for word in word_counter:
        if word_counter[word] >= 2:
            new_words.append({'text': word, 'size': word_counter[word]}) 
    return new_words

def retrieve_tweet_dates(intervalle = None):
    tweets_table = mongo.db.tweets
    buffer = []
    for tweet in tweets_table.find({"session_id": session['last_session']}):
        buffer.append(time.mktime(datetime.datetime.strptime(tweet['tweet_object']['created_at'], '%a %b %d %H:%M:%S +0000 %Y').timetuple())-7200)
    return date_to_int(buffer, intervalle)

def date_to_int(tweet_dates, new_intervalle = None):
    if tweet_dates:
        start_date = int(min(tweet_dates))
        stop_date = int(max(tweet_dates))

        if new_intervalle is None:
            if stop_date-start_date >= 172800:#intervalle de 2 jours
                intervals = 172800
            elif stop_date-start_date >= 86400:#intervalle de 1 jour
                intervals = 86400
            elif stop_date-start_date >= 43200:#intervalle de 12 heures
                intervals = 43200
            elif stop_date-start_date >= 3600:#intervalle de 1 heure
                intervals = 3600
            elif stop_date-start_date >= 600:#intervalle de 10 minutes
                intervals = 600
            elif stop_date-start_date >= 60:#intervalle de 1 minute
                intervals = 60
            elif stop_date-start_date >= 30:#intervalle de 30 secondes
                intervals = 30
            else:
                intervals = 10
        else:
            intervals = int(new_intervalle)
        new_freq = []
        if start_date == stop_date:
            new_freq.append({'freq': 1, 'start_date': start_date, 'stop_date': start_date + intervals})
        for x in range(start_date, stop_date, intervals):
            if x == stop_date:
                break
            new_freq.append({'freq': count_date(tweet_dates, x, x+intervals), 'start_date': x, 'stop_date': x+intervals})
        return new_freq

def count_date(buffer, d, f):
    count = 0
    for i in range(len(buffer)):
        if buffer[i] >= d and buffer[i] <= f:
            count = count + 1
    return count


def retrieve_tweets_by_date(start,stop):
    tweets_table = mongo.db.tweets
    tweet_text = ""
    count = 0
    for tweet in tweets_table.find({"session_id": session['last_session']}):
        count = count +1
        d = datetime.datetime.strptime(tweet['tweet_object']['created_at'], '%a %b %d %H:%M:%S +0000 %Y')
        if time.mktime(d.timetuple())-7200 >= float(start) and time.mktime(d.timetuple())-7200 <= float(stop):
            if "full_text" in tweet['tweet_object']:
                tweet_text = tweet_text + " " + tweet['tweet_object']["full_text"]
            else:
                tweet_text = tweet_text + " " + tweet['tweet_object']["text"]
    return word_splitter(tweet_text)

def getTweets(start, stop):
    tweets_table = tweets_by_session_id(session['last_session'])
    buffer = []
    for tweet in tweets_table:
        d = datetime.datetime.strptime(tweet['tweet_object']['created_at'], '%a %b %d %H:%M:%S +0000 %Y')
        if time.mktime(d.timetuple())-7200 >= float(start) and time.mktime(d.timetuple())-7200 <= float(stop):
            buffer.append({'id': tweet['tweet_object']['id_str']})
    return buffer