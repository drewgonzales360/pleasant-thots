#!/usr/bin/env python
# Module: consumer.py
from __future__ import absolute_import, print_function

import os
import json
import pandas as pd
import matplotlib.pyplot as plt

coinbase_access_token  = '7bbdddf0428d743b220ce82a8a9baedd4983314d6a231f5aa40ff4515a7b0860'
coinbase_refresh_token = '2c7733ce0da4436165e6866244b9c00157bb678f7140b7504da6e824870b3cc1'

from coinbase.wallet.client import OAuthClient
import thread, time
from coinmarketcap import Market

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
