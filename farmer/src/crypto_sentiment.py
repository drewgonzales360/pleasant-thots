#!/usr/bin/env python
from __future__ import absolute_import, print_function

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

import os
import json
import pandas as pd
import matplotlib.pyplot as plt

from textblob import TextBlob

# Connect to Twitter
twitter_consumer_key = 'aMZWIC8rUe1SA3SFxCigpC9Au'
twitter_consumer_secret = 'xe4A5H3CkQUJsVYtZTunu3pga5uZOKYObLYFfXBzvTao66cUFn'
twitter_access_token = '799736116563746816-7D0xWdZFJgUjdkOA6yXI6xPt0YWgcIc'
twitter_access_token_secret = 'Y4ufiEiL0jbZqPD3WrO7W40OEPZ28LHbbuUwr3YyojYE1'

from textblob import TextBlob

coinbase_access_token  = '7bbdddf0428d743b220ce82a8a9baedd4983314d6a231f5aa40ff4515a7b0860'
coinbase_refresh_token = '2c7733ce0da4436165e6866244b9c00157bb678f7140b7504da6e824870b3cc1'

from coinbase.wallet.client import OAuthClient
import thread, time
from coinmarketcap import Market

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
            print ('Sentiment:', tweet_sentiment)
            new_tweet = {'text':tweet_txt, 'sentiment':tweet_sentiment, 'retweet_count': tweet['retweet_count']}
            with open ('test.json', 'a') as test_file:
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
    #sentiment.append(analysis.sentiment.polarity)
    return new_analysis

def start_streaming(thread_name):
    print (thread_name + ' starting')
    l = StdOutListener()

    auth = OAuthHandler(twitter_consumer_key, twitter_consumer_secret)
    auth.set_access_token(twitter_access_token, twitter_access_token_secret)

    stream = Stream(auth, l)
    stream.filter(track = ['ripple', 'xrp'])

def start_analysis(thread_name):
    time.sleep(60)
    print (thread_name + ' starting')

    while True:
        with open('test.json', 'r') as sentiment_file:
            sentiment_data = [json.loads(sentiment_node) for sentiment_node in sentiment_file]

        with open('test.json', 'wr+') as sentiment_file:
            sentiment_file.truncate(0)

        sum_sentiment = 0
        for sentiment_node in sentiment_data:
            sum_sentiment = sum_sentiment + sentiment_node['sentiment'] 
  
        avg_sentiment = sum_sentiment/len(sentiment_data)
        print ("Number of Tweets Processed: ", len(sentiment_data))
        print ("Average Sentiment: ", avg_sentiment)
        decision = trade_decision(avg_sentiment)
        print ("Trade Decision: ", decision)
        price = get_current_price()
        print ("Current Price (USD): ", price)
        tweets_analysis = {'num_process': len(sentiment_data), 'avg_sentiment': avg_sentiment, 'decision': decision, 'current_price_usd': price}
        with open('analaysis.json', 'a') as analysis_file:
            json.dump(tweets_analysis, analysis_file)
            analysis_file.write(os.linesep)
    
        time.sleep(60)

def trade_decision(avg_sentiment):
    if avg_sentiment <= 1 and avg_sentiment >= 0.5:
        decision = "BUY"
    elif avg_sentiment > -0.5 and avg_sentiment < 0.5:
        decision = "HOLD"
    elif avg_sentiment <= -0.5 and avg_sentiment >= -1:
        decision = "SELL"
    return decision

def get_current_price():
    coinmarketcap = Market()
    currency = coinmarketcap.ticker('Ripple', limit=1, convert='USD')
    currency = currency[0]
    return (currency['price_usd'])

if __name__ == '__main__':
    print ('Starting Script')
    
#    client = OAuthClient(coinbase_access_token, coinbase_refresh_token, api_version='2018-04-23')
#    currency_code='USD'

    try:
        thread.start_new_thread(start_streaming, ('thread-1', ))
        thread.start_new_thread(start_analysis, ('thread-2', ))
    except:
        print ("Error: unable to start thread")
    while 1:
        pass
