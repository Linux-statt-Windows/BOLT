#!/bin/env python3

import urllib.request
import json

URL = 'http://api.linux-statt-windows.org/infos.json'

def callback():
    return '/lsw', get_forum


def get_forum(inp):
    rqst = urllib.request.urlopen(URL)
    data = json.loads(rqst.read().decode('utf-8'))
    forum = data[0]['forum']
    return forum['name']\
            + '\n\nShort URL: ' + forum['short_url'] \
            + '\nLong URL: ' + forum['long_url'] \
            + '\nDE URL: ' + forum['de_url'] \
            + '\nEU URL:' + forum['eu_url'] \
            + '\nFAQ: ' + forum['faq_url'] \
            + '\nRegeln: ' + forum['rules_url']


def get_help():
    return '\n/lsw: Bekomme den Link zu unserer Homepage.'


if __name__ == '__main__':
    print(get_forum())
