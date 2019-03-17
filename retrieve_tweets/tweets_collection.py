from myapp import mongo, app
import re, collections
from flask import session
from stop_words import get_stop_words
import datetime, time
from textblob import TextBlob
import unicodedata

def getText(data):
    # Try for extended text of original tweet, if RT'd (streamer)
    try: text = data['retweeted_status']['extended_tweet']['full_text']
    except:
        # Try for extended text of an original tweet, if RT'd (REST API)
        try: text = data['retweeted_status']['full_text']
        except:
            # Try for extended text of an original tweet (streamer)
            try: text = data['extended_tweet']['full_text']
            except:
                # Try for extended text of an original tweet (REST API)
                try: text = data['full_text']
                except:
                    # Try for basic text of original tweet if RT'd
                    try: text = data['retweeted_status']['text']
                    except:
                        # Try for basic text of an original tweet
                        try: text = data['text']
                        except:
                            # Nothing left to check for
                            text = ''
    return text

def clean_text(tweet_text):
    tweet_text = tweet_text.lower()
    normalized = unicodedata.normalize('NFD', tweet_text)
    tweet_text = u"".join([c for c in normalized if not unicodedata.combining(c)])
    tweet_text.replace("-", " ")
    tweet_text.replace("'", " ")
    tweet_text = re.sub(r'[^\w\s]', '', tweet_text)
    tweet_text = re.sub(r'\s\s+', ' ', tweet_text)
    tweet_text = re.sub(r'http\S+', '', tweet_text)
    tweet_text = re.sub(r'[0-9]', '', tweet_text)
    return tweet_text

def stock_tweets(tweet, stream):
    if stream:
        tweets_table = mongo.db.tweets
        data = tweet._json
        tweet_text = getText(data)
        tweet_text = clean_text(tweet_text)
        words = tweet_text.split(" ")
        stop_words = get_stop_words('fr') + get_stop_words('en')
        words = [word for word in words if word not in stop_words and 'RT' not in word and len(word) > 2]
        field = {'split': words}
        data.update(field)
        tweets_table.insert({'session_id': session['last_session'], 'tweet_object': data})
    else:
        tweets_table = mongo.db.tweets
        data = tweet
        tweet_text = getText(data)
        tweet_text = clean_text(tweet_text)
        words = tweet_text.split(" ")
        stop_words = get_stop_words('fr')
        words = [word for word in words if word not in stop_words and 'RT' not in word and len(word) > 2]
        field = {'split': words}
        data.update(field)
        if tweets_by_session_id(session['last_session']).count() > 0:
            for tw in tweets_by_session_id(session['last_session']):
                if tweet['id_str'] == tw['tweet_object']['id_str']:
                    return 0
            tweets_table.insert({'session_id': session['last_session'], 'tweet_object': data})
            return 1
        else:
            tweets_table.insert({'session_id': session['last_session'], 'tweet_object': data})
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

def tweet_by_geo():
    tweets_table = mongo.db.tweets
    tweets_geo_table = []
    for tweet in tweets_table.find({"session_id": session['last_session']}):
        if 'coordinates' in tweet['tweet_object']:
            if tweet['tweet_object']['coordinates'] is not None:
                tweets_geo_table.append(tweet['tweet_object']['coordinates'])
    return tweets_geo_table

def clean_tweet(tweet):
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

def tweet_by_text_analysis():
    tweets_table = mongo.db.tweets
    positif = 0
    neutre = 0
    negatif = 0
    polarity_values = []
    for tweet in tweets_table.find({"session_id": session['last_session']}):
        if 'text' in tweet['tweet_object']:
            if tweet['tweet_object']['text'] is not None:
                text = clean_tweet(tweet['tweet_object']['text'])
                sentiment_value = TextBlob(text)
                if sentiment_value.polarity > 0.00:
                    positif = positif+1
                if sentiment_value.polarity == 0:
                    neutre = neutre+1
                if sentiment_value.polarity < 0.00:
                    negatif = negatif+1
    polarity_values.append(negatif)
    polarity_values.append(neutre)
    polarity_values.append(positif)
    return polarity_values

def retrieve_all_tweets_text():
    tweets_table = mongo.db.tweets
    if 'last_session' in session:
        tweet_text = []
        for tweet in tweets_table.find({"session_id": session['last_session']}):
            if 'split' in tweet['tweet_object']:
                if tweet['tweet_object']['split'] is not None:
                    for tweet_split in tweet['tweet_object']['split']:
                        tweet_text.append(tweet_split)
        return word_splitter(tweet_text)


def word_splitter(words):
    new_words = []
    word_counter = collections.Counter(words)
    for word in word_counter:
        if word_counter[word] > 2:
            if word != '':
                new_words.append({'text': word, 'size': word_counter[word]})
    return new_words

def retrieve_tweet_dates(intervalle = None):
    tweets_table = mongo.db.tweets
    buffer = []
    for tweet in tweets_table.find({"session_id": session['last_session']}):
        buffer.append(time.mktime(datetime.datetime.strptime(tweet['tweet_object']['created_at'], '%a %b %d %H:%M:%S +0000 %Y').timetuple()))
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
        if time.mktime(d.timetuple())>= float(start) and time.mktime(d.timetuple())<= float(stop):
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
        if time.mktime(d.timetuple()) >= float(start) and time.mktime(d.timetuple()) <= float(stop):
            buffer.append({'id': tweet['tweet_object']['id_str']})
    return buffer