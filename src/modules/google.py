#!/bin/env python3

import urllib.request
import json
import re

def callback():
    return '/google', get_google


def get_google(key):
    data = {
            "v":"1.0",
            "q":key
            }
    data = urllib.parse.urlencode(data)
    rqst = urllib.request.urlopen('http://ajax.googleapis.com/ajax/services/search/web?' + data)
    data = json.loads(rqst.read().decode('utf-8'))
    results = data['responseData']['results']
    pr = 'Ergebnisse: \n'
    for r in results:
        title = re.sub('<b>', '', re.sub('<\/b>', '', r['title']))
        pr += '\n' + title \
                 + ' - ' + r['url']
    return pr


def get_help():
    return '\n/google [suchbegriff]: Zeigt die  ersten Suchergebnisse der Google-Suche'


if __name__ == '__main__':
    print(get_google('test'))
