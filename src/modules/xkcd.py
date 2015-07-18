#!/bin/env python3

import urllib.request
import json

URL = 'http://dynamic.xkcd.com/random/comic/'
f = '/var/lib/bolt/xkcd.png'

def callback():
    return '/xkcd', get_xkcd


def get_xkcd(inp):
    rqst = urllib.request.urlopen(URL)
    rqst = urllib.request.urlopen(rqst.geturl() + 'info.0.json')
    img_rqst = urllib.request.urlopen(json.loads(rqst.read().decode('utf-8'))['img'])
    img = open(f, 'wb')
    img.write(img_rqst.read())
    img.close()
    return f


def get_help():
    return '\n/xkcd: Zeigt einen zufälligen Comic von XKCD'


if __name__ == '__main__':
    print(get_xkcd(0))
