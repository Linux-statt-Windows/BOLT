#!/bin/env python3

import urllib.request
import json
import time

URL = 'https://linux-statt-windows.org/api/category/7/lsw-support'

def callback():
    return '', get_reminder


def get_reminder(inp):
    rqst = urllib.request.urlopen(URL)
    data = json.loads(rqst.read().decode('utf-8'))
    name = data['name']
    related_topics = []
    output = name + '\n'
    for t in data['topics']:
        if int(t['timestamp'][:3]) >= (int(time.time()) - 3600):
            related_topics.append(t)
    for t in related_topics:
        output += '\nTitle: ' + t['title'] \
                + '\nURL: https://linux-statt-windows.org/topic/' + t['slug'] \
                + '\n\n'
    if related_topics != []:
        return output
    else:
        return None


def get_help():
    return ''


def get_repeat():
    return 1 
    return hourly


if __name__ == '__main__':
    print(get_reminder(0))
