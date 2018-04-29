FROM docker pull resin/qemux86-alpine-python:2.7

RUN pip install tweepy TextBlob coinbase coinmarketcap

RUN \
apt-get update; \
apt-get upgrade; \
apt-get install python-pandas; \
apt-get install python-matplotlib
RUN mkdir -p /pleasant-thots/logs

WORKDIR /pleasant-thots
