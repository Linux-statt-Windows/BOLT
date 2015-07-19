#!/bin/env python3

import urllib.request
import json

URL = 'http://api.linux-statt-windows.org/infos.json'

def callback():
    return '', get_reminder


def get_reminder(inp):
    rqst = urllib.request.urlopen(URL)
    data = json.loads(rqst.read().decode('utf-8'))
    # TODO:
    #  - logic for event handling
    return 'data'


def get_help():
    return ''


def get_repeat():
    return 1


if __name__ == '__main__':
    print(get_reminder(0))
