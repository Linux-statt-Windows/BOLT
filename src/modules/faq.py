#!/bin/env python3

import urllib.request
import json

URL = 'http://api.linux-statt-windows.org/infos.json'

def get_faq():
    rqst = urllib.request.urlopen(URL)
    data = json.loads(rqst.read().decode('utf-8'))
    faq = data[0]['faq']
    return faq['name'] \
            + '\n\nURL: ' + faq['url']


if __name__ == '__main__':
    print(get_faq())
