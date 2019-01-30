import tweepy

consumer_key = "DT4qrp9j1ttwfsoXWtbhYlwOl"
consumer_secret = "g8X2I3cTbqv5A44zuz5UWa2s7nRUXPfWWRZpUwWOGSahy3tIoU"
access_token = "955782108341063680-0WOfWNVnHv1uXBOpl2Gp3KDgS6HgHSk"
access_token_secret = "CY8bhHMS2sBeript7PjVo2Zw0azfvwwNnmo1GVutOXHSk"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth, wait_on_rate_limit= True, wait_on_rate_limit_notify=True)