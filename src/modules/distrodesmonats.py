#!/bin/env python3

import urllib.request
import json

URL = 'http://api.linux-statt-windows.org/infos.json'

def get_distro():
    rqst = urllib.request.urlopen(URL)
    data = json.loads(rqst.read().decode('utf-8'))
    distro = data[0]['distro_month']
    return distro['name'] \
            + '\n\nMonat: ' + distro['month'] \
            + '\nURL: ' + distro['url']  

if __name__ == '__main__':
    get_distro()
