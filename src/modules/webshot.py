#!/bin/env python3

import urllib.request
import json

URL = 'http://api.screenshotmachine.com/?'
KEY = ''
f = '/var/lib/bolt/webshot.png'

def callback():
    return '/webshot', get_webshot


def get_webshot(myinp):
    inp = ''
    for i in myinp:
        inp += i
    #inp = {
    #        "url":inp,
    #        "key":KEY
    #        }
    #data = urllib.parse.urlencode(inp)
    #print(data)
    data = 'key=' + KEY + '&size=FULL' + '&url=' + inp
    rqst = urllib.request.urlopen(URL + data)
    data = rqst.read()
    img = open(f, 'wb')
    img.write(data)
    img.close()
    return f


def get_help():
    return '\n/cmd: helptext'


if __name__ == '__main__':
    print(get_webshot('http://www.google.com'))
