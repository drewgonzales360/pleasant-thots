#!/usr/bin/env python
# Module: start_senti.py
import tweepy, time, os, sys

import thread
import json

import producer
import consumer
import logging

logging.basicConfig(level=logging.DEBUG, 
                    format='%(asctime)s %(levelname)s %(message)s',
                    filename='farmer/logs/senti_crypto.log',
                    filemode='w')

# Connect to Twitter
twitter_consumer_key = 'aMZWIC8rUe1SA3SFxCigpC9Au'
twitter_consumer_secret = 'xe4A5H3CkQUJsVYtZTunu3pga5uZOKYObLYFfXBzvTao66cUFn'
twitter_access_token = '799736116563746816-7D0xWdZFJgUjdkOA6yXI6xPt0YWgcIc'
twitter_access_token_secret = 'Y4ufiEiL0jbZqPD3WrO7W40OEPZ28LHbbuUwr3YyojYE1'

exp_config = 'farmer/logs/experiments.json'

#if __name__ == '__main__':
def start():
    print ('Starting Program')

    logging.debug(exp_config)

    with open(exp_config, 'r') as exp_config_file:
        exp_configs = [json.loads(exp_node) for exp_node in exp_config_file]

    for exp_node in exp_configs:
        exp_name = exp_node['exp_name']
        search_query = exp_node['search_query']

        logging.debug(exp_name)
        logging.debug(search_query)

        try:
            thread.start_new_thread(producer.start_streaming, 
                                        (exp_name,
                                        twitter_consumer_key,
                                        twitter_consumer_secret,
                                        twitter_access_token,
                                        twitter_access_token_secret, 
                                        search_query, ))
#            thread.start_new_thread(consumer.start_analysis, 
#                                    ('consumer', crypto_currency, ))
        except:
            logging.error("Unable to start thread")
#        while 1:
#            pass
