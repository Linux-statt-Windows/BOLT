#!/bin/env python3

import urllib.request
import json

URL = 'http://api.linux-statt-windows.org/infos.json'

def get_github():
    rqst = urllib.request.urlopen(URL)
    data = json.loads(rqst.read().decode('utf-8'))
    github = data[0]['github']
    return'Github' \
            + '\n\nURL: ' + github['url'] \
            + '\nShort URL: ' + github['short_url']


if __name__ == '__main__':
    print(get_github())
