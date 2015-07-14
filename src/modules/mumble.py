#!/bin/env python3

import urllib.request
import json

URL = 'http://api.linux-statt-windows.org/infos.json'

def callback():
    return '/lsw Mumble', get_mumble


def get_mumble(inp):
    rqst = urllib.request.urlopen(URL)
    data = json.loads(rqst.read().decode('utf-8'))
    mumble = data[0]['mumble']
    return 'Mumble\n\n' \
        + 'Direct Link: ' + mumble['direct_url'] \
        + '\nURL: ' + mumble['url'] \
        + '\nPort: ' + str(mumble['port'])

if __name__ == '__main__':
    print(get_mumble())
