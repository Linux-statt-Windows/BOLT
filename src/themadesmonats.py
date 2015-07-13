#!/bin/env python3

import urllib.request
import datetime
import json
import re

def monthly_topic():
    now = datetime.datetime.now()
    names = ['Januar', 'Februar', 'März', 'April', 'Mai', 'Juni', 'Juli', 'August', 'September', 'Oktober', 'November', 'Dezember']
    url = 'https://linux-statt-windows.org/api/category/49/thema-des-monats'
    rqst = urllib.request.urlopen(url)
    data = json.loads(rqst.read().decode('utf-8'))
    for topic in data['topics']:
        if topic['title'].startswith('[' + names[now.month - 1] + ']'):
            title = re.sub('\[[a-zA-Z]*\]\s', '', topic['title'])
            return title


if __name__ == '__main__':
    monthly_topic()
