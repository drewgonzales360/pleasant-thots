# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os, json

from django.http import HttpResponse
from django.shortcuts import render

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
    sentiment = round(analysis_data['avg_sentiment'])
    decision = analysis_data['decision']
    return HttpResponse(json.dumps(analysis_data,indent=4, sort_keys=True))

