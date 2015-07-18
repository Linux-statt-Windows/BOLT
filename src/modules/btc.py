#!/bin/env python3

import urllib.request
import json

URL = 'https://api.bitcoinaverage.com/ticker/global/EUR/'

def callback():
    return '/btc', get_btc


def get_btc(inp):
    rqst = urllib.request.urlopen(URL)
    data = json.loads(rqst.read().decode('utf-8'))
    return 'Bitcoin/Euro'\
                + '\n\nBieter: ' + str(data['bid']) \
                + '\nKäufer: ' + str(data['ask']) \
                + '\n\nLetzte Akualisierung: ' + str(data['timestamp'])


def get_help():
    return '\n/btc: Zeigt den akutellen Bitcoin<->Euro Kurs an'


if __name__ == '__main__':
    print(get_btc(0))
