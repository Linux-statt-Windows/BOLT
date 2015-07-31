#!/bin/env python3

import urllib.request
import datetime
import json
import re

URL = 'http://api.linux-statt-windows.org/infos.json'

def callback():
    return '/lsw thema', monthly_topic


def monthly_topic(inp):
    now = datetime.datetime.now()
    names = ['Januar', 'Februar', 'März', 'April', 'Mai', 'Juni', 'Juli', 'August', 'September', 'Oktober', 'November', 'Dezember']
    rqst = urllib.request.urlopen(URL)
    data = json.loads(rqst.read().decode('utf-8'))
    topic = data[0]['topic_month']
    return topic['name'] \
            + '\n\nMonat: ' + topic['month'] \
            + '\nURL: ' + topic['url']


def get_help():
    return '\n/lsw Thema: Finde heraus, was das aktuelle thema des Monats ist.'


if __name__ == '__main__':
    monthly_topic()
