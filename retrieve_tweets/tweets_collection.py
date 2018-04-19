from myapp import mongo, app
import json, bson
import re, collections

from flask import session, jsonify


from flask import session
from stop_words import get_stop_words
import datetime, pytz, time

def stock_tweets(tweet):
    #print(tweet)
    tweets_table = mongo.db.tweets
    tweets_table.insert({'session_id': session['last_session'], 'tweet_object': tweet._json})

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
    #print(tweet_text)
    tweet_text = re.sub(r'[^\w\s]', '', tweet_text)
    tweet_text = re.sub(r'\s\s+', ' ', tweet_text)
    pattern = re.compile('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    pattern.sub('', tweet_text)
    words = tweet_text.split(" ")
    new_words = []
    stop_words = get_stop_words('fr') + get_stop_words('en')
   # print(tweet_text)
    for word in words:
        if 'RT' == word.lower() or word in stop_words:
            words.remove(word)
    #print(words)
    word_counter = collections.Counter(words)
    for word in word_counter:
        if word_counter[word] >= 2:
            new_words.append({'text': word, 'size': word_counter[word]})
    print(new_words)
    return new_words

def retrieve_tweet_dates(start_date = None, stop_date=None):
    tweets_table = mongo.db.tweets
    buffer = []
    if start_date is not None and stop_date is not None:
        start_date = datetime.datetime.strptime(start_date, '%a %b %d %H:%M:%S +0000 %Y').replace(
            tzinfo=pytz.UTC)
        stop_date = datetime.datetime.strptime(stop_date, '%a %b %d %H:%M:%S +0000 %Y').replace(
            tzinfo=pytz.UTC)
        for tweet in tweets_table.find({"session_id": session['last_session']}):
            d = datetime.datetime.strptime(tweet['tweet_object']['created_at'], '%a %b %d %H:%M:%S +0000 %Y').replace(
                tzinfo=pytz.UTC)
            if time.mktime(d.timetuple()) >= float(start_date) and time.mktime(d.timetuple()) <= float(stop_date):
                print(time.mktime(d.timetuple()))
                buffer.append(time.mktime(d.timetuple()))
    else:
        for tweet in tweets_table.find({"session_id": session['last_session']}):
            d = datetime.datetime.strptime(tweet['tweet_object']['created_at'], '%a %b %d %H:%M:%S +0000 %Y').replace(tzinfo=pytz.UTC)
            buffer.append(time.mktime(d.timetuple()))
    print(buffer)
    return date_to_int(buffer, start_date,stop_date)


def date_to_int(tweet_dates,start = None,stop = None):
    if tweet_dates:
        if start is None and stop is None:
            start_date = int(min(tweet_dates))
            stop_date = int(max(tweet_dates))
        else:
            start_date = start
            stop_date = stop

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
        start_date = int(min(tweet_dates))
        stop_date = int(max(tweet_dates))
        new_freq = []
        for x in range(start_date, stop_date, intervals):
            if x == stop_date:
                break
            new_freq.append({'freq': count_date(tweet_dates, x, x+intervals), 'start_date': x, 'stop_date': x+intervals})
        #print(new_freq)
        return new_freq


def count_date(buffer, d, f):
    count = 0
    for i in range(len(buffer)):
        # print("tweet : " + str(buffer[i]) + " debut : " + str(d) + " fin : " + str(f))
        if buffer[i] >= d and buffer[i] <= f:
            count = count + 1
    return count


def retrieve_tweets_by_date(start,stop):
    tweets_table = mongo.db.tweets
    tweet_text = ""
    count = 0
    for tweet in tweets_table.find({"session_id": session['last_session']}):
        count = count +1
        d = datetime.datetime.strptime(tweet['tweet_object']['created_at'], '%a %b %d %H:%M:%S +0000 %Y').replace(tzinfo=pytz.UTC)
        if time.mktime(d.timetuple()) >= float(start) and time.mktime(d.timetuple()) <= float(stop):
            tweet_text = tweet_text + " " + tweet['tweet_object']["full_text"]
    print("count : " + str(count))
    return word_splitter(tweet_text)

def getTheMostRT(start, stop):
    tweets_table = tweets_by_session_id(session['last_session'])
    twot = []
    max = 0
    for tweet in tweets_table:
        d = datetime.datetime.strptime(tweet['tweet_object']['created_at'], '%a %b %d %H:%M:%S +0000 %Y').replace(
            tzinfo=pytz.UTC)
        if time.mktime(d.timetuple()) >= float(start) and time.mktime(d.timetuple()) <= float(stop):
            if tweet['tweet_object']['retweet_count'] >= max:
                twot = tweet['tweet_object']
    buffer = []
    buffer.append({'user': twot['user']["name"], 'nbRt': twot['retweet_count'], 'text': twot['full_text'] })
    print(buffer)
    return buffer