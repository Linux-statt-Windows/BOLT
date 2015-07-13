#!/bin/env python3

import urllib.request
import json

URL = 'http://api.linux-statt-windows.org/infos.json'

def get_mumble():
    rqst = urllib.request.urlopen(URL)
    data = json.loads(rqst.read().decode('utf-8'))
    mumble = data[0]['mumble']
    return mumble['direct_url'], mumble['url'], mumble['port']


if __name__ == '__main__':
    print(get_mumble())
