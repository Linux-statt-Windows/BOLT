#!/bin/env python3

import urllib.request
import json

URL = 'http://api.qrserver.com/v1/create-qr-code/?'
f = '/var/lib/bolt/qr.png'

def callback():
    return '/qr', get_qr


def get_qr(inp):
    text = ''
    for i in inp:
        text += i
    data = {
            "size":"600x600",
            "data":text
            }
    data = urllib.parse.urlencode(data)
    rqst = urllib.request.urlopen(URL + data)
    data = rqst.read()
    img = open(f, 'wb')
    img.write(data)
    img.close()
    return f


def get_help():
    return '\n/qr [text]: Erstellt einen qr-Code'


if __name__ == '__main__':
    print(get_qr('test'))
