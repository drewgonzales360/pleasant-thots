#!/usr/bin/env python
from __future__ import absolute_import, print_function

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

import json
import pandas as pd
import matplotlib.pyplot as plt

from textblob import TextBlob

# Connect to Twitter
consumer_key = 'aMZWIC8rUe1SA3SFxCigpC9Au'
consumer_secret = 'xe4A5H3CkQUJsVYtZTunu3pga5uZOKYObLYFfXBzvTao66cUFn'

access_token = '799736116563746816-7D0xWdZFJgUjdkOA6yXI6xPt0YWgcIc'
access_token_secret = 'Y4ufiEiL0jbZqPD3WrO7W40OEPZ28LHbbuUwr3YyojYE1'

class StdOutListener(StreamListener):
    """ A listener handles tweets that are received from the stream.
    This is a basic listener that just prints received tweets to stdout.
    """
    def on_data(self, data):
        #print("preProcessed:" + data)
        readData(data)
        return True

    def on_error(self, status):
        print(status)

def readData(data):
    #print ("postProcessed:")
    tweet = json.loads(data)
    #print (json.dumps(tweet, indent=4, sort_keys=True))
    print("text:" + tweet['text'])
    tweet_txt = tweet['text']
    get_tweet_sentiment(tweet_txt)
    #with open ("test.txt", "a") as myfile:
    #    myfile.write(tweet_txt.encode('utf-8'))

def get_tweet_sentiment(tweet_txt):
    analysis = TextBlob(tweet_txt)
    print ("Analysis:" + str(analysis.sentiment.polarity))

if __name__ == '__main__':
    print ('Starting Script')
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    stream = Stream(auth, l)
    stream.filter(track=['litecoin'])

