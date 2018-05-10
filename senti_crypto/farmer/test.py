#!/usr/bin/env python
# Module: test.py
import tweepy, time, os, sys

import thread
import json

import consumer
import logging

import unittest

#logging.basicConfig(level=logging.DEBUG, 
#                    format='%(asctime)s %(levelname)s %(message)s',
#                    filename='farmer/logs/senti_crypto.log',
#                    filemode='w')

# Connect to Twitter
#twitter_consumer_key = 'aMZWIC8rUe1SA3SFxCigpC9Au'
#twitter_consumer_secret = 'xe4A5H3CkQUJsVYtZTunu3pga5uZOKYObLYFfXBzvTao66cUFn'
#twitter_access_token = '799736116563746816-7D0xWdZFJgUjdkOA6yXI6xPt0YWgcIc'
#twitter_access_token_secret = 'Y4ufiEiL0jbZqPD3WrO7W40OEPZ28LHbbuUwr3YyojYE1'

#exp_config = 'farmer/logs/experiments.json'
#experiment_twitter = False

class test_consumer_methods(unittest.TestCase):

    def test_get_transact_shares(self):
        transact_shares = consumer.get_transact_shares(0.123)
        self.assertEqual(transact_shares, 1)
        transact_shares = consumer.get_transact_shares(-0.123)
        self.assertEqual(transact_shares, 1)
        transact_shares = consumer.get_transact_shares(0.623)
        self.assertEqual(transact_shares, 6)
        transact_shares = consumer.get_transact_shares(-0.623)
        self.assertEqual(transact_shares, 6)
        transact_shares = consumer.get_transact_shares(1)
        self.assertEqual(transact_shares, 10)
        transact_shares = consumer.get_transact_shares(-1)
        self.assertEqual(transact_shares, 10)

    def test_get_sentiment_range(self):
        sentiment_range = consumer.get_sentiment_range(10)
        self.assertEqual(sentiment_range, 5)
        sentiment_range = consumer.get_sentiment_range(20)
        self.assertEqual(sentiment_range, 10)
        sentiment_range = consumer.get_sentiment_range(1)
        self.assertEqual(sentiment_range, 0)
        sentiment_range = consumer.get_sentiment_range(-1)
        self.assertRaises(ValueError)
        sentiment_range = consumer.get_sentiment_range(30)
        self.assertRaises(ValueError)

    def test_trade_sim_buy(self):
        decision = "BUY"
        price = 10
        avg_sentiment = 0.6
        exp_shares = 0
        exp_balance = 100
        exp_value = 0
        sentiment_range = 5
        exp_data = consumer.trade_sim(decision, price, avg_sentiment, exp_shares, exp_balance, exp_value, sentiment_range)
        self.assertEqual(exp_data['exp_shares'], 1)
        self.assertEqual(exp_data['exp_balance'], 90)
        self.assertEqual(exp_data['exp_value'], 100)
        
        decision = "BUY"
        price = 10
        avg_sentiment = 0.7
        exp_shares = 0
        exp_balance = 100
        exp_value = 100
        sentiment_range = 5
        exp_data = consumer.trade_sim(decision, price, avg_sentiment, exp_shares, exp_balance, exp_value, sentiment_range)
        self.assertEqual(exp_data['exp_shares'], 2)
        self.assertEqual(exp_data['exp_balance'], 80)
        self.assertEqual(exp_data['exp_value'], 100)
 
        decision = "BUY"
        price = 10
        avg_sentiment = -0.6
        exp_shares = 0
        exp_balance = 100
        exp_value = 100
        sentiment_range = 5
        exp_data = consumer.trade_sim(decision, price, avg_sentiment, exp_shares, exp_balance, exp_value, sentiment_range)
        self.assertEqual(exp_data['exp_shares'], 0)
        self.assertEqual(exp_data['exp_balance'], 100)
        self.assertEqual(exp_data['exp_value'], 100)

        decision = "BUY"
        price = 10
        avg_sentiment = 0.4
        exp_shares = 0
        exp_balance = 100
        exp_value = 100
        sentiment_range = 5
        exp_data = consumer.trade_sim(decision, price, avg_sentiment, exp_shares, exp_balance, exp_value, sentiment_range)
        self.assertEqual(exp_data['exp_shares'], 0)
        self.assertEqual(exp_data['exp_balance'], 100)
        self.assertEqual(exp_data['exp_value'], 100)
 
    def test_trade_sim_hold(self):
        decision = "HOLD"
        price = 10
        avg_sentiment = 0.4
        exp_shares = 0
        exp_balance = 100
        exp_value = 0
        sentiment_range = 5
        exp_data = consumer.trade_sim(decision, price, avg_sentiment, exp_shares, exp_balance, exp_value, sentiment_range)
        self.assertEqual(exp_data['exp_shares'], 0)
        self.assertEqual(exp_data['exp_balance'], 100)
        self.assertEqual(exp_data['exp_value'], 100)

    def test_trade_sim_sell(self):
        decision = "SELL"
        price = 10
        avg_sentiment = -0.6
        exp_shares = 1
        exp_balance = 90
        exp_value = 100
        sentiment_range = 5
        exp_data = consumer.trade_sim(decision, price, avg_sentiment, exp_shares, exp_balance, exp_value, sentiment_range)
        self.assertEqual(exp_data['exp_shares'], 0)
        self.assertEqual(exp_data['exp_balance'], 100)
        self.assertEqual(exp_data['exp_value'], 100)

        decision = "SELL"
        price = 10
        avg_sentiment = -0.6
        exp_shares = 0
        exp_balance = 90
        exp_value = 90
        sentiment_range = 5
        exp_data = consumer.trade_sim(decision, price, avg_sentiment, exp_shares, exp_balance, exp_value, sentiment_range)
        self.assertEqual(exp_data['exp_shares'], 0)
        self.assertEqual(exp_data['exp_balance'], 90)
        self.assertEqual(exp_data['exp_value'], 90)

        decision = "SELL"
        price = 10
        avg_sentiment = -0.8
        exp_shares = 1
        exp_balance = 90
        exp_value = 100
        sentiment_range = 1
        exp_data = consumer.trade_sim(decision, price, avg_sentiment, exp_shares, exp_balance, exp_value, sentiment_range)
        self.assertEqual(exp_data['exp_shares'], 0)
        self.assertEqual(exp_data['exp_balance'], 100)
        self.assertEqual(exp_data['exp_value'], 100)
        
        decision = "SELL"
        price = 20
        avg_sentiment = -0.6
        exp_shares = 2
        exp_balance = 80
        exp_value = 120
        sentiment_range = 5
        exp_data = consumer.trade_sim(decision, price, avg_sentiment, exp_shares, exp_balance, exp_value, sentiment_range)
        self.assertEqual(exp_data['exp_shares'], 1)
        self.assertEqual(exp_data['exp_balance'], 100)
        self.assertEqual(exp_data['exp_value'], 120)
        
        decision = "SELL"
        price = 10
        avg_sentiment = -0.6
        exp_shares = 1
        exp_balance = 90
        exp_value = 100
        sentiment_range = 2
        exp_data = consumer.trade_sim(decision, price, avg_sentiment, exp_shares, exp_balance, exp_value, sentiment_range)
        self.assertEqual(exp_data['exp_shares'], 0)
        self.assertEqual(exp_data['exp_balance'], 100)
        self.assertEqual(exp_data['exp_value'], 100)

if __name__ == '__main__':
    unittest.main()
