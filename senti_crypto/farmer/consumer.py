#!/usr/bin/env python
# Module: consumer.py
from __future__ import absolute_import, print_function

import os
import os.path
import json
import pandas as pd
import matplotlib.pyplot as plt
import logging

coinbase_access_token  = '7bbdddf0428d743b220ce82a8a9baedd4983314d6a231f5aa40ff4515a7b0860'
coinbase_refresh_token = '2c7733ce0da4436165e6866244b9c00157bb678f7140b7504da6e824870b3cc1'

from coinbase.wallet.client import OAuthClient
import thread, time
from coinmarketcap import Market

current_milli_time = lambda: int(round(time.time() * 1000))

def start_analysis(exp_node):
    time.sleep(exp_node['poll_time'])

    exp_name = exp_node['exp_name']
    currency = exp_node['currency']
    start_balance = exp_node['start_balance']
    logging.debug(exp_name + 'consumer starting')

    exp_producer_path = 'farmer/logs/' + exp_name + '-producer.json'
    exp_consumer_path = 'farmer/logs/' + exp_name + '-consumer.json'

    price = get_current_price(currency)
    create_experiment(price, exp_name, currency, start_balance)

    while True:
        with open(exp_consumer_path, 'r') as exp_consumer_file:
            exp_consumer_data = [json.loads(exp_consumer_node) for exp_consumer_node in exp_consumer_file]
            exp_consumer_data = exp_consumer_data[-1]

        try: 
            with open(exp_producer_path, 'r') as exp_producer_file:
                exp_producer_data = [json.loads(exp_producer_node) for exp_producer_node in exp_producer_file]
        except:
            logging.error("No %s Producer File Found" % exp_name)
            pass

        # after storing everything in memory delete contents of producer file to save memory
        with open(exp_producer_path, 'wr+') as exp_producer_file:
            exp_producer_file.truncate(0)
    
        #make sure exp_producer_data exists
        if exp_producer_data != None:
            avg_sentiment = get_avg_sentiment(exp_producer_data)
        else:
            pass
        
        if avg_sentiment == 0:
            logging.debug("Nothing to process, passing and waiting")
            pass
        else:
            sentiment_range = get_sentiment_range(exp_node['sentiment_range'])
            decision = get_trade_decision(avg_sentiment, sentiment_range)
            price = get_current_price(currency)

            #if first pass create ref_shares, ref_balance, and ref_value
            ref_value = (int(exp_consumer_data['ref_shares']) * float(price)) + exp_consumer_data['ref_balance']
            exp_data = trade_sim(decision, 
                                    price, 
                                    avg_sentiment, 
                                    exp_consumer_data['exp_shares'],
                                    exp_consumer_data['exp_balance'], 
                                    exp_consumer_data['exp_value'],
                                    sentiment_range) 
            logging.debug(json.dumps(exp_data))
            #logging.debug("Experiment Balance: ", exp_data['exp_balance'])
            transaction = {'exp_name': exp_name,
                            'currency': currency,
                            'current_price': price,
                            'ref_balance': exp_consumer_data['ref_balance'],
                            'ref_shares': exp_consumer_data['ref_shares'],
                            'ref_value': ref_value,
                            'exp_balance': exp_data['exp_balance'],
                            'exp_shares': exp_data['exp_shares'],
                            'exp_value': exp_data['exp_value'],
                            'decision': decision,
                            'sentiment': avg_sentiment,
                            'num_process': len(exp_producer_data),
                            'timestamp_ms': current_milli_time()}

            with open(exp_consumer_path, 'a') as exp_consumer_file:
                json.dump(transaction, exp_consumer_file)
                exp_consumer_file.write(os.linesep)
        time.sleep(exp_node['poll_time'])

def get_sentiment_range(sentiment_range):
    if sentiment_range > 20 or sentiment_range < 1:
        return ValueError("Outside Acceptable Sentiment Range 0-20")
    else:
        return round(sentiment_range/2)

def get_avg_sentiment(exp_data):
    sum_sentiment = 0
    for exp_node in exp_data:
        sum_sentiment = sum_sentiment + exp_node['sentiment']

    if sum_sentiment == 0:
        return 0
    else:
        return (sum_sentiment/len(exp_data))

def get_trade_decision(avg_sentiment, sentiment_range):
    sentiment_range /= 10

    if avg_sentiment <= 1 and avg_sentiment >= sentiment_range:
        decision = "BUY"
    elif avg_sentiment > -sentiment_range and avg_sentiment < sentiment_range:
        decision = "HOLD"
    elif avg_sentiment <= -sentiment_range and avg_sentiment >= -1:
        decision = "SELL"
    return decision

def create_experiment(price, exp_name, currency, start_balance):
    logging.debug("Creating Expiriment File: " + exp_name)
    exp_consumer_path = 'farmer/logs/%s-consumer.json' % exp_name

    #if file exists remove it and start over
    if os.path.exists(exp_consumer_path):
        os.remove(exp_consumer_path)

    #make sure start balance is not 0
    if start_balance != 0:
        ref_shares = round(float(start_balance) / float(price))
        ref_balance = start_balance - (ref_shares * float(price))
        if ref_balance <= 0:
            ref_shares = ref_shares - 1
            ref_balance = start_balance - (ref_shares * float(price))
            ref_value = ref_balance + (ref_shares * float(price))
        else:
            ref_value = ref_balance + (ref_shares * float(price))
    else:
        ref_shares = 0
        ref_value = 0
        ref_balance = start_balance
        logging.error(exp_name + " reference baseline not created")

    first_transaction = {'exp_name': exp_name,
                        'currency': currency,
                        'current_price': price,
                        'ref_balance': ref_balance,
                        'ref_shares': ref_shares,
                        'ref_value': ref_value,
                        'exp_balance': start_balance,
                        'exp_shares': 0,
                        'exp_value': start_balance,
                        'decision': 'HOLD',
                        'num_process': 0,
                        'timestamp_ms': current_milli_time()}
    logging.debug(first_transaction)
    with open (exp_consumer_path, 'a') as exp_file:
        json.dump(first_transaction, exp_file)
        exp_file.write(os.linesep)

#<TODO> Fix negative transaction of shares exp_shares can neever be negative but it's happening
def trade_sim(decision, price, avg_sentiment, exp_shares, exp_balance, exp_value, sentiment_range):
    transact_shares = get_transact_shares(avg_sentiment) - sentiment_range
    if decision == "BUY":
        amount = float(transact_shares) * float(price)
        if amount > exp_balance:
            logging.debug("Cannot Buy, ammount: %f is greater than wallet balance " % (amount))
            pass
        else:
            exp_balance = exp_balance - amount
            exp_shares = exp_shares + transact_shares
    elif decision == "HOLD":
        pass
    elif decision == "SELL":
        if exp_shares == 0:
            logging.debug('Number of Shares is 0, cannot sell')
            pass
        elif transact_shares >= exp_shares:
            logging.debug("transact_shares:", str(transact_shares), " >= exp_shares:", str(exp_shares))
            transact_shares = exp_shares
            amount = float(exp_shares) * float(price)
            exp_shares = 0
            exp_balance = exp_balance + amount
        elif transact_shares < exp_shares:
            logging.debug("transact_shares:", str(transact_shares), " < exp_shares:", str(exp_shares))
            amount = float(transact_shares) * float(price)
            exp_balance = exp_balance + amount
            exp_shares = exp_shares - transact_shares
        else:
            logging.error("transaction error")

    #get current total value of my wallet
    exp_value = (exp_shares * float(price)) + float(exp_balance)
    
    return {'exp_shares':exp_shares, 'exp_balance':exp_balance, 'exp_value':exp_value}

def get_transact_shares(avg_sentiment):
    if avg_sentiment == 1 or avg_sentiment == -1:
        transact_shares = 10
    else:
        transact_shares = int(str(abs(avg_sentiment))[2])
    return transact_shares

def get_current_price(currency):
    coinmarketcap = Market()
    price = coinmarketcap.ticker(currency, limit=1, convert='USD')[0]    
    return (price['price_usd'])
