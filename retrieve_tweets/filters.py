from retrieve_tweets.tweets_collection import *
from myapp import *
import tweepy
from retrieve_tweets.tweets_collection import *
from flask import render_template

stream_stop = False  # Variable globale pour permettre le partage de la variable entre les 2 threads.

class Stream(tweepy.StreamListener):
    def on_status(self, status):
        if not stream_stop:
            stock_tweets(status, True)
        else:
            return False

def filter(keywords=None, geocode=None, stream=False, startdate=None, stopdate=None, user=None, starttime=None, stoptime=None, language=None, tweets_batch=None):
    if geocode is not "":
        # Passe d'une chaîne de caractère en un tableau de floats (chaque élément séparé d'une virgule)
        geocode = [float(s) for s in geocode.split(",")]
    if stream:# Le cas où l'utilisateur veut des tweets en direct
        global stream_stop
        stream_stop = False

        if user is not "":
            user = getIdByUser(user)

        stream_o = tweepy.Stream(auth=api.auth, listener=Stream())
        stream_o.filter(locations=geocode, track=[keywords], languages=[language], follow=[user])
    else:# Le cas des tweets datés
        minid = getMinId() # Voir la description de cette fonction directement à la définition de celle ci
        query = keywords + ' -filter:retweets'# Pour ne pas avoir les copies des tweets (les tweets RT de quelqu'un)
        if user != "": # Ajout de l'utilisateur si il existe dans la session
            query = query + " from:@" + user

        """ Gestion des dates heures des tweets à récupérer 
            startdate et stopdate sont les variables transmises depuis le formulaire
            start et stop sont les fusions des dates et heures du formulaire
            
            Pour le cas où la date de début et la date de fin sont égales, nous mettons la date de fin à un jour de plus pour avoir une intervalle correct pour la fonction Cursor
            start_d et stop_d sont la conversion des dates et heures en secondes pour faciliter la comparaison     
        """
        start = startdate + ' ' + starttime
        stop = stopdate + ' ' + stoptime
        if startdate != '' and stopdate != '': # Si nous avons des dates il faut comparer la date de chaque tweet récupéré avec ces dates là
            start_d = time.mktime(datetime.datetime.strptime(start, '%Y-%m-%d %H:%M').timetuple())
            stop_d = time.mktime(datetime.datetime.strptime(stop, '%Y-%m-%d %H:%M').timetuple())
            if minid != -1:
                for tweet in tweepy.Cursor(api.search, q=query, lang=language, tweet_mode="extended", since=startdate, max_id=minid).items(int(tweets_batch)):
                    created_at = time.mktime(datetime.datetime.strptime(str(tweet.created_at), '%Y-%m-%d %H:%M:%S').timetuple())
                    if created_at >= start_d and created_at <= stop_d:
                        stock_tweets(tweet._json, False)
            else:
                for tweet in tweepy.Cursor(api.search, q=query, lang=language, tweet_mode="extended", since=startdate).items(int(tweets_batch)):
                    created_at = time.mktime(datetime.datetime.strptime(str(tweet.created_at), '%Y-%m-%d %H:%M:%S').timetuple())
                    if created_at >= start_d and created_at <= stop_d:
                        stock_tweets(tweet._json, False)
        else: # si il n'y a pas de dates alors nous stockons les premiers tweets venus sans comparer
            if minid != -1:
                for tweet in tweepy.Cursor(api.search, q=query, lang=language, tweet_mode="extended", max_id=minid).items(int(tweets_batch)):
                    stock_tweets(tweet._json, False)
            else:
                for tweet in tweepy.Cursor(api.search, q=query, lang=language, tweet_mode="extended").items(int(tweets_batch)):
                    stock_tweets(tweet._json, False)

@app.route('/session/stream/stop')
def stopStream():
    global stream_stop
    stream_stop = True
    return render_template('session_create_form.html')  # On devrait rien retourner (ou page vide) car Ajax

def getIdByUser(userName):
    return api.get_user(userName).id_str


"""
    Nous avons implémenté cette fonction pour avoir l'id minimale des tweets dans la base de données
    Ceci nous est important pour la fonction de récupération, surtout pour re récupérer sur une session déjà crée
    L'id min permet de ne pas reprendre les mêmes tweets que la première récupération 
"""
def getMinId():
    tweets_table = tweets_by_session_id(session['last_session'])
    if tweets_table.count() > 0:
        minid = 10019764059058708484050050
        for tweet in tweets_table:
            if tweet['tweet_object']['id'] < minid:
                minid = tweet['tweet_object']['id']
    else:
        minid = -1
    return minid
