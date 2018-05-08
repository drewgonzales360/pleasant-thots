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

experiment_twitter = False

#if __name__ == '__main__':
def start():
    print ('Starting Program')
    logging.debug(exp_config)

    experiments = []
    search_query = []

    with open(exp_config, 'r') as exp_config_file:
        exp_configs = [json.loads(exp_node) for exp_node in exp_config_file]

    #grab all experiments and store into memory
    for exp_node in exp_configs:

        #check if twitter experiments and store into format for thread starting
        if exp_node['exp_producer'] or exp_node['exp_consumer'] == 'twitter':
            experiments.append(exp_node)
            for query in exp_node['search_query']:
                search_query.append(query)
        
            experiment_twitter = True

        #remove duplicates from list
        old_search_query = search_query
        search_query = []
        for query in old_search_query:
            if query not in search_query:
                search_query.append(query)

    logging.debug(experiments)
    logging.debug(search_query)
    print (experiments)
    print (search_query)

    #check if twitter experiments and start threads to run experiments
    #twitter only allows 1 max 2 connections so right now there is only
    #one connection, maybe if infra needs we can scale to two threads for 
    #pulling tweets, on the consumer side there is one thread per 
    #experiment. 
    if experiment_twitter == True:
        try:
            thread.start_new_thread(producer.start_streaming, 
                                        (experiments,
                                        twitter_consumer_key,
                                        twitter_consumer_secret,
                                        twitter_access_token,
                                        twitter_access_token_secret, 
                                        search_query, ))
            for exp_node in experiments:
                thread.start_new_thread(consumer.start_analysis, 
                                        (exp_node, ))
                pass
        except:
            logging.error("Unable to start thread")
#        while 1:
#            pass
