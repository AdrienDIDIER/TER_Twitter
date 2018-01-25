from auth import *

def tweet_ten_times(i):
    while i < 10:
        api.update_status(i)
        i += 1

i = 1
tweet_ten_times(i)
