#!/bin/env python3

import urllib.request
import json

URL = 'http://www.omdbapi.com/?'

def callback():
    return '/omdb', get_omdb


def get_omdb(inp):
    search = ''
    for i in inp:
        search += i + ' '
    search = search.lstrip(' ')
    data = {
            't':search,
            'plot':'full',
            'r':'json'
            }
    data = urllib.parse.urlencode(data)
    rqst = urllib.request.urlopen(URL + data)
    data = json.loads(rqst.read().decode('utf-8'))
    return 'Titel: ' + data['Title'] \
            + '\nJahr: ' + data['Year'] \
            + '\nRating: ' + data['imdbRating'] \
            + '\n\n' + data['Plot'] \
            + '\n\nPoster: ' + data['Poster']


def get_help():
    return '\n/omdb [Titel]: Sucht Ergebnisse auf omdb für den Titel'


if __name__ == '__main__':
    print(get_omdb(['Iron', 'Man']))
