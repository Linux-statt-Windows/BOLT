#!/bin/env python3

import urllib.request
import json

URL = 'http://api.linux-statt-windows.org/infos.json'

def get_forum():
    rqst = urllib.request.urlopen(URL)
    data = json.loads(rqst.read().decode('utf-8'))
    forum = data[0]['forum']
    return forum['name'], forum['short_url'], forum['long_url'], forum['de_url'], forum['eu_url'], forum['faq_url'], forum['rules_url']


if __name__ == '__main__':
    print(get_forum())
