#!/bin/env python3

import urllib.request
import json

URL = 'http://api.linux-statt-windows.org/infos.json'

def get_fb():
    rqst = urllib.request.urlopen(URL)
    data = json.loads(rqst.read().decode('utf-8'))
    fb = data[0]['fb']
    return fb['group_url'], fb['short_group_url'], fb['site_url']


if __name__ == '__main__':
    print(get_fb())
