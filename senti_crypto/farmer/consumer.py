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

current_milli_time = lambda: int(round(time.time() * 1000))

def start_analysis(thread_name, crypto_currency):
    time.sleep(60)
    print (thread_name + ' starting')
    
    price = get_current_price(crypto_currency)
    create_reference(price)

    while True:
        with open('farmer/logs/tweet_logs.json', 'r') as sentiment_file:
            sentiment_data = [json.loads(sentiment_node) for sentiment_node in sentiment_file]

        with open('farmer/logs/tweet_logs.json', 'wr+') as sentiment_file:
            sentiment_file.truncate(0)

        sum_sentiment = 0
        for sentiment_node in sentiment_data:
            sum_sentiment = sum_sentiment + sentiment_node['sentiment'] 
  
        if sum_sentiment == 0:
            print ("Nothing to process, passing and waiting")
            pass
        else:
            avg_sentiment = sum_sentiment/len(sentiment_data)
            #avg_sentiment = -0.654
            print ("Number of Tweets Processed: ", len(sentiment_data))
            print ("Average Sentiment: ", avg_sentiment)
            decision = trade_decision(avg_sentiment)
            print ("Trade Decision: ", decision)
            price = get_current_price(crypto_currency)
            print ("Current Price (USD): ", price)

            update_reference(price)
            trade_sim(decision, price, avg_sentiment)

            tweets_analysis = {'num_process': len(sentiment_data),
                                'avg_sentiment': avg_sentiment,
                                'decision': decision,
                                'current_price_usd': price,
                                'currency': crypto_currency,
                                'timestamp_ms': current_milli_time()}

            with open('farmer/logs/analysis.json', 'a') as analysis_file:
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

def create_reference(price):
    print ("Creating Reference File")
    with open ('farmer/logs/reference.json', 'r') as reference_file:
        reference_data = [json.loads(reference_node) for reference_node in reference_file]
        reference_data = reference_data[-1]

    wallet_balance = float(reference_data['wallet_balance'])
    transact_shares = round(wallet_balance / float(price))
    amount = float(price) * transact_shares
    if reference_data['number_of_shares'] > 0:
        transact_shares = reference_data['number_of_shares']
    elif amount > wallet_balance:
        transact_shares = transact_shares - 1
        amount = float(price) * transact_shares
        wallet_balance = wallet_balance - amount
    else:
        wallet_balance = wallet_balance - amount

    current_value = (transact_shares * float(price)) + float(wallet_balance)

    print ("transact_shares: ", transact_shares)
    new_transaction = {'wallet_balance': wallet_balance,
                        'currency':reference_data['currency'],
                        'current_price': price,
                        'number_of_shares': transact_shares,
                        'current_value': current_value,
                        'timestamp_ms': current_milli_time()}
    print (new_transaction)
    with open ('farmer/logs/reference.json', 'a') as reference_file:
        json.dump(new_transaction, reference_file)
        reference_file.write(os.linesep)

def update_reference(price):
    print ("Updating Reference File")
    with open ('farmer/logs/reference.json', 'r') as reference_file:
        reference_data = [json.loads(reference_node) for reference_node in reference_file]
        reference_data = reference_data[-1]

    current_value = (int(reference_data['number_of_shares']) * float(price)) + float(reference_data['wallet_balance'])
    new_reference = {'wallet_balance': reference_data['wallet_balance'],
                        'currency':reference_data['currency'],
                        'current_price': price,
                        'number_of_shares': reference_data['number_of_shares'],
                        'current_value': current_value,
                        'timestamp_ms': current_milli_time()}
    print (new_reference)
    with open ('farmer/logs/reference.json', 'a') as reference_file:
        json.dump(new_reference, reference_file)
        reference_file.write(os.linesep)

def trade_sim(decision, price, avg_sentiment):
    with open ('farmer/logs/wallet.json', 'r') as wallet_file:
        wallet_data = [json.loads(wallet_node) for wallet_node in wallet_file]
        wallet_data = wallet_data[-1]
        wallet_balance = float(wallet_data['wallet_balance'])
        number_of_shares = int(wallet_data['number_of_shares'])

    print (wallet_data)
    if decision == "BUY":
        transact_shares = get_transact_shares(avg_sentiment) - 5
        amount = float(transact_shares) * float(price)
        print ('amount: ', amount)
        if amount > wallet_balance:
            print ("Cannot Buy, ammount: %f is greater than wallet balance " % (amount))
            pass
        else:
            wallet_balance = wallet_balance - amount
            number_of_shares = number_of_shares + transact_shares
    elif decision == "HOLD":
        pass
    elif decision == "SELL":
        transact_shares = get_transact_shares(avg_sentiment) - 5
        
        if number_of_shares == 0:
            print ('Number of Shares is 0, cannot sell')
            pass
        elif transact_shares >= number_of_shares:
            transact_shares = number_of_shares
            amount = float(number_of_shares) * float(price)
            number_of_shares = 0
            wallet_balance = wallet_balance + amount
        else:
            print ('wallet balance: ', wallet_balance)
            amount = float(transact_shares) * float(price)
            wallet_balance = wallet_balance + amount
            number_of_shares = number_of_shares - transact_shares

    #get current total value of my wallet
    current_value = (number_of_shares * float(price)) + float(wallet_balance)

    new_transaction = {'wallet_balance': wallet_balance,
                        'currency':wallet_data['currency'],
                        'current_price': price,
                        'number_of_shares': number_of_shares,
                        'current_value': current_value,
                        'timestamp_ms': current_milli_time()}
    print (new_transaction)
    with open ('farmer/logs/wallet.json', 'a') as wallet_file:
        json.dump(new_transaction, wallet_file)
        wallet_file.write(os.linesep)

def get_transact_shares(avg_sentiment):
    transact_shares = int(str(abs(avg_sentiment))[2])
    print ("Shares: ", transact_shares)
    return transact_shares

def get_current_price(crypto_currency):
    crypto_currency = crypto_currency[0]
    coinmarketcap = Market()
    currency = coinmarketcap.ticker(crypto_currency, limit=1, convert='USD')
    currency = currency[0]
    return (currency['price_usd'])
