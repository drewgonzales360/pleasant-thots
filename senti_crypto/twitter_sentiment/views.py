# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os, json

from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader

def index(request):
    analysis_data = {}
    file_location = os.getcwd() + '/farmer/logs/analysis.json'
    try:
        with open (file_location, 'r') as analysis_file:
            analysis_data = [json.loads(analysis_node) for analysis_node in analysis_file]
            analysis_data = analysis_data[-1]
    except:
        print ("Could not open: ", file_location)

    currency = analysis_data['currency']
    currency_output = {'data': currency[1], 'txt': 'CURRENCY'}
    sentiment = round(analysis_data['avg_sentiment'], 2)
    sentiment_output = {'data': sentiment, 'txt': 'SENTIMENT'}
    decision = analysis_data['decision']
    decision_output = {'data': decision, 'txt': 'DECISION' }
    senti_list = []
    senti_list.append(currency_output)
    senti_list.append(sentiment_output)
    senti_list.append(decision_output)
    context = {
        'senti_list': senti_list,
    }
    #return HttpResponse(template.render(decision, request))
    return render(request, 'twitter_sentiment/index.html', context)

