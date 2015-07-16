#!/bin/env python3

import urllib.request
import re

URL = 'http://api.mathjs.org/v1/?'

def callback():
    return '/calc', get_calc


def get_calc(myinp):
    inp = ''
    for i in myinp:
        inp += i
    inp = re.sub('\s', '', inp)
    data = {
            'expr':inp,
            'precision':'10'
            }
    data = urllib.parse.urlencode(data)
    rqst = urllib.request.urlopen(URL + data)
    result = rqst.read().decode('utf-8')
    return str(result)


def get_help():
    return '\n/calc [Term]: Berechnet das Ergebnis des eingegebenen Terms'


if __name__ == '__main__':
    print(get_calc(['(5+5*5)^2']))
