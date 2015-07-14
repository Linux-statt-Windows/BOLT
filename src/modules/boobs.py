#!/bin/env python3

import urllib.request
import json

def callback():
    return '/boobs', get_boobs
        

def get_boobs(inp):
    rqst = urllib.request.urlopen('http://api.oboobs.ru/noise/1')
    data = json.loads(rqst.read().decode('utf-8'))
    return 'http://media.oboobs.ru/' + data[0]['preview']


def get_help():
    return ''


if __name__ == '__main__':
    print(get_boobs())
