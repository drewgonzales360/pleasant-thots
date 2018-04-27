import tweepy, time, os, sys

import thread

import producer
import consumer

#crypto_currency = ['bitcoin', 'BTC', 'ripple', 'XRP', 'ETH', 'ETC']
crypto_currency = ['ripple', 'XRP']

# Connect to Twitter
twitter_consumer_key = 'aMZWIC8rUe1SA3SFxCigpC9Au'
twitter_consumer_secret = 'xe4A5H3CkQUJsVYtZTunu3pga5uZOKYObLYFfXBzvTao66cUFn'
twitter_access_token = '799736116563746816-7D0xWdZFJgUjdkOA6yXI6xPt0YWgcIc'
twitter_access_token_secret = 'Y4ufiEiL0jbZqPD3WrO7W40OEPZ28LHbbuUwr3YyojYE1'

if __name__ == '__main__':
    print ('Starting Script')
    try:
        thread.start_new_thread(producer.start_streaming, ('producer',
            twitter_consumer_key,
            twitter_consumer_secret,
            twitter_access_token,
            twitter_access_token_secret, 
            crypto_currency, )
            )
        thread.start_new_thread(consumer.start_analysis, ('consumer',
            crypto_currency, )
            )
    except:
        print ("Error: unable to start thread")
    while 1:
        pass
