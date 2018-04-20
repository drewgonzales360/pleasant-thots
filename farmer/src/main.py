#!/usr/bin/env python
################################################################################
# The Remembral
#
# This bot will post new updates to twitter every 5 minutes and respond
# to any one that replys. The replys will happen at the next time a tweet is
# made
################################################################################
import tweepy, time, os, sys

# Connect to Twitter
consumer_key = 'aMZWIC8rUe1SA3SFxCigpC9Au'
consumer_secret = 'xe4A5H3CkQUJsVYtZTunu3pga5uZOKYObLYFfXBzvTao66cUFn'
access_token = '799736116563746816-7D0xWdZFJgUjdkOA6yXI6xPt0YWgcIc'
access_token_secret = 'Y4ufiEiL0jbZqPD3WrO7W40OEPZ28LHbbuUwr3YyojYE1'
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)
user = api.me()

FIVE_MINUTES=300
TEN_SECONCDS=10
BAR="\n===========================\n"
NON_BMP_MAP = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
################################################################################

def find():
    """
    Checks if anyone has sent any replys to @margaritashita. Replys to mentions
    only once using global variable REPLIED_TO.
    """
    if not os.path.isdir('log'):
        os.mkdir('log')

    while True:
        searchResults = api.search(q="@realDonaldTrump", lang="en", tweet_mode='extended')
        for r in searchResults:
            handle = str(r.user.name).translate(NON_BMP_MAP)

            # Let's not grab retweets
            retweet = r._json.get("retweeted_status")
            if retweet is None:
                out = open('log/trump.txt', 'a+')
                print(r.full_text, end=BAR)
                out.write(str(r.full_text) + BAR)
                out.close()
        time.sleep(TEN_SECONCDS)

if __name__ == '__main__':
    print('Starting %s with username %s with %s friends.' % ("Drew", user.name,str(user.friends_count)))
    find()
