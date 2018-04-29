FROM resin/rpi-raspbian

RUN apt-get update && apt-get install -y  apt-utils pip;

RUN sudo apt-get install libfreetype6-dev pkg-config libpng12-dev
RUN \
pip install --upgrade pip; \
apt-get install python-pandas; \
apt-get install python-matplotlib; \
pip install --upgrade matplotlib;

RUN mkdir -p /pleasant-thots
RUN pip install tweepy TextBlob coinbase coinmarketcap

WORKDIR /pleasant-thots
