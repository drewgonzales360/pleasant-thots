FROM resin/raspberry-pi-python:3.5.2

RUN pip install tweepy

RUN mkdir /pleasant-thots
ADD src/main.py /pleasant-thots/main.py

WORKDIR /pleasant-thots

CMD ["python", "main.py"]
