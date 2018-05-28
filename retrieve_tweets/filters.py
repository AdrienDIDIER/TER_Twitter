from retrieve_tweets.tweets_collection import *
from myapp import *
from tweepy_auth import *
from retrieve_tweets.tweets_collection import *
from flask import render_template

stream_stop = False  # Variable globale pour permettre le partage de la variable entre les 2 threads.

class Stream(tweepy.StreamListener):
    def on_status(self, status):
        if not stream_stop:
            stock_tweets(status)
        else:
            return False

def filter(keywords=None, geocode=None, stream=False, startdate=None, stopdate=None, user=None, starttime=None, stoptime=None, language=None, tweets_batch=None):
    if geocode is not "":
        # Passe d'une chaîne de caractère en un tableau de floats (chaque élément séparé d'une virgule)
        geocode = [float(s) for s in geocode.split(",")]
    if stream:
        global stream_stop
        stream_stop = False

        if user is not "":
            user = getIdByUser(user)

        stream_o = tweepy.Stream(auth=api.auth, listener=Stream())
        stream_o.filter(locations=geocode, track=[keywords], languages=[language], follow=[user])
    else:
        geocode = None # TODO: FIX (Filtrer par geocode) et fix language
        query = keywords + ' -filter:retweets'
        if user != "":
            query = query + " from:@" + user
        start = startdate + ' ' + starttime
        stop = stopdate + ' ' + stoptime
        if startdate != '' and stopdate != '':
            if startdate == stopdate:
                stop_1 = datetime.datetime.strptime(stopdate, "%Y-%m-%d")
                stopdate = stop_1 + datetime.timedelta(days=1)
            print(query)
            start_d = time.mktime(datetime.datetime.strptime(start, '%Y-%m-%d %H:%M').timetuple())
            stop_d = time.mktime(datetime.datetime.strptime(stop, '%Y-%m-%d %H:%M').timetuple())
        searched_tweets = []
        last_id = -1

        while(len(searched_tweets) < int(tweets_batch)):
            try:
                new_tweets = api.search(q=query, tweet_mode="extended", count=100, lang=language, until=stopdate, since=startdate)
                if not new_tweets:
                    break
                searched_tweets.extend(new_tweets)
            except tweepy.TweepError as e:
                print(e)
                break
        for i in searched_tweets:
            created_at = time.mktime(datetime.datetime.strptime(str(i.created_at), '%Y-%m-%d %H:%M:%S').timetuple())
            if created_at >= start_d and created_at <= stop_d:
                tweets = dict(i._json)
                print(tweets['created_at'])
                stock_tweets(tweets)

@app.route('/session/stream/stop')
def stopStream():
    global stream_stop
    stream_stop = True
    return render_template('session_create_form.html')  # On devrait rien retourner (ou page vide) car Ajax

def getIdByUser(userName):
    return api.get_user(userName).id_str
