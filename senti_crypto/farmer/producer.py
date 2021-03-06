#!/usr/bin/env python
# Module: producer.py

from __future__ import absolute_import, print_function

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

import os, time
import logging
import json
import pandas as pd
import matplotlib.pyplot as plt

from textblob import TextBlob

#<TODO> Componetize Twitter Producer

class StdOutListener(StreamListener):
    """ A listener handles tweets that are received from the stream.
    This is a basic listener that just prints received tweets to stdout.
    """
    def __init__(self, exp_name):
        self.exp_name = exp_name

    def on_data(self, data):
        readData(data, self.exp_name)
        return True

    def on_error(self, status):
        logging.error(status)

def readData(data, experiments):
    tweet = json.loads(data)
    retweet = None
    try:
        retweet = tweet['retweeted_status']
    except:
        pass

    #get rid of retweets
    if retweet is None:
        tweet_txt = tweet['text']
        retweet_count = tweet['retweet_count']

        #logging.debug(tweet_txt)

        tweet_sentiment = get_tweet_sentiment(tweet_txt, retweet_count)
        
        for exp in experiments:
           for query in exp['search_query']:
               if query in tweet_txt and tweet_sentiment !=0:

                    #get rid of 0 tweet sentiments (not helpful for decisions)
                    new_tweet = {'exp_name': exp['exp_name'], 
                                    'text':tweet_txt,
                                    'sentiment':tweet_sentiment,
                                    'retweet_count': retweet_count,
                                    'timestamp_ms': tweet['timestamp_ms']}

                    logging.debug(new_tweet)

                    exp_data_file = 'farmer/logs/' + exp['exp_name'] + '-producer.json'
                    with open (exp_data_file, 'a') as exp_data_output:
                        json.dump(new_tweet, exp_data_output)
                        exp_data_output.write(os.linesep)

def get_tweet_sentiment(tweet_txt, retweet_count):
    analysis = TextBlob(tweet_txt)
    if retweet_count == 0:
        new_analysis = analysis.sentiment.polarity
    else:
        new_analysis = analysis.sentiment.polarity * retweet_count 
    return new_analysis

def start_streaming(experiments, 
        twitter_consumer_key, 
        twitter_consumer_secret, 
        twitter_access_token, 
        twitter_access_token_secret, 
        search_query):

    logging.debug('all producer experiments starting')
    l = StdOutListener(experiments)
    auth = OAuthHandler(twitter_consumer_key, twitter_consumer_secret)
    auth.set_access_token(twitter_access_token, twitter_access_token_secret)

    stream = Stream(auth, l)
    stream.filter(track = search_query, async=True, languages=["en"])

