#!/bin/env python3

import urllib.request
import json

def callback():
    return '/ddgo', get_ddgo
        

def get_ddgo(key):
    data = {
            "format":"json",
            "q":key,
            "no_html":"1"
            }
    data = urllib.parse.urlencode(data)
    rqst = urllib.request.urlopen('http://api.duckduckgo.com/?' + data)
    data = json.loads(rqst.read().decode('utf-8'))
    a = 'Ergebnisse\n'
    for topic in data['RelatedTopics']:
        a += '\n' + topic['FirstURL'] + ' - ' + topic['Text']
    return a


if __name__ == '__main__':
    print(get_ddgo('link local'))
