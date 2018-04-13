from myapp import mongo, app
import json, bson
import re, collections
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
    tweets_table = tweets_by_session_id(session['last_session'])
    tweet_text = ""
    for tweet in tweets_table:
        tweet_text = tweet_text + " " + tweet['tweet_object']['full_text']
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
    return new_words

def retrieve_tweet_dates():
    tweets_table = mongo.db.tweets;
    buffer = []
    for tweet in tweets_table.find({"session_id": session['last_session']}):
        buffer.append(tweet['tweet_object']['created_at'])
    return date_to_int(buffer)


def date_to_int(tweet_dates):
    buffer = []
    for date in tweet_dates:
        d = datetime.datetime.strptime(date, '%a %b %d %H:%M:%S +0000 %Y').replace(tzinfo=pytz.UTC)
        buffer.append(time.mktime(d.timetuple()))
    print(buffer)
    start_date = int(min(buffer))
    stop_date = int(max(buffer))
    print(start_date)
    print(stop_date)
    new_freq = []
    for x in range(start_date, stop_date,60):
        if x == stop_date:
            break
        new_freq.append({'freq': count_date(buffer, x, x+60), 'start_date': x, 'stop_date': x+60})
    print(new_freq)
    return new_freq


def count_date(buffer, d, f):
    count = 0
    for i in range(len(buffer)):
        print("tweet : " + str(buffer[i]) + " debut : " + str(d) + " fin : " + str(f))
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
