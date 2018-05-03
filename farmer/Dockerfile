FROM resin/rpi-raspbian

RUN apt-get update && apt-get install -y  apt-utils;
RUN apt-get install -y python;
RUN curl --silent --show-error --retry 5 https://bootstrap.pypa.io/get-pip.py | sudo python;
RUN apt-get install -y libfreetype6-dev pkg-config libpng12-dev
RUN apt-get install -y gcc
RUN \
pip install --upgrade pip; \
apt-get install python-pandas; \
apt-get install python-matplotlib; 
RUN apt-get install -y python-tk
RUN mkdir -p /pleasant-thots
RUN pip install tweepy TextBlob coinbase coinmarketcap

WORKDIR /pleasant-thots
