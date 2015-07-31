#!/bin/env python3

import urllib.request
import json

URL = 'http://api.linux-statt-windows.org/infos.json'

def callback():
    return '/lsw facebook', get_fb


def get_fb(inp):
    rqst = urllib.request.urlopen(URL)
    data = json.loads(rqst.read().decode('utf-8'))
    fb = data[0]['fb']
    return 'Facebook Gruppen' \
            + '\n\nGruppe: ' + fb['group_url'] \
            + '\nGruppe(short URL): ' + fb['short_group_url'] \
            + '\nFacebook-Seite: ' + fb['site_url']


def get_help():
    return '\n/lsw Facebook: Bekomme die Links zu unserer Facebook Gruppe und Seite.'


if __name__ == '__main__':
    print(get_fb())
