#!/usr/bin/env python
# Module: producer.py

from __future__ import absolute_import, print_function

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

import os, time
import json
import pandas as pd
import matplotlib.pyplot as plt

from textblob import TextBlob

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
    tweet = json.loads(data)
    #print (json.dumps(tweet, indent=4, sort_keys=True))
    retweet = None
    try:
        #print (tweet['retweeted_status'])
        retweet = tweet['retweeted_status']
        #print (retweet)
        #print ("Found Repeat")
    except:
        pass
        #print ("No Repeat Status")

    #get rid of retweets
    if retweet is None:
        tweet_txt = tweet['text']
        #print ('============================')
        #print ('text: ', tweet_txt)
        #print ('retweet_count:', tweet['retweet_count'])
        retweet_count = tweet['retweet_count']
        tweet_sentiment = get_tweet_sentiment(tweet_txt, retweet_count)

        #get rid of 0 tweet sentiments (not helpful for decisions)
        if tweet_sentiment != 0:
            #print ('Sentiment:', tweet_sentiment, 'Text: ', tweet_txt)
            print ('Sentiment:', tweet_sentiment)
            new_tweet = {'text':tweet_txt, 'sentiment':tweet_sentiment, 'retweet_count': retweet_count, 'timestamp_ms': tweet['timestamp_ms']}
            with open ('farmer/logs/tweet_logs.json', 'a') as test_file:
                json.dump(new_tweet, test_file)
                test_file.write(os.linesep)

def get_tweet_sentiment(tweet_txt, retweet_count):
    analysis = TextBlob(tweet_txt)
    #print ("Analysis:" + str(analysis.sentiment.polarity))
    if retweet_count == 0:
        new_analysis = analysis.sentiment.polarity
    else:
        new_analysis = analysis.sentiment.polarity * retweet_count 
    #print ("With Weight", new_analysis)
    return new_analysis

def start_streaming(thread_name, 
        twitter_consumer_key, 
        twitter_consumer_secret, 
        twitter_access_token, 
        twitter_access_token_secret, 
        crypto_currency):
    print (thread_name + ' starting')
    l = StdOutListener()
    auth = OAuthHandler(twitter_consumer_key, twitter_consumer_secret)
    auth.set_access_token(twitter_access_token, twitter_access_token_secret)

    stream = Stream(auth, l)
    stream.filter(track = crypto_currency)

