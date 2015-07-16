#!/bin/env python3

import urllib.request
import json
import re

URL = 'http://apimeme.com/meme?'
f = '/var/lib/bolt/meme.jpg'

def callback():
    return '/meme', get_meme


def get_meme(inp):
    meme_type, top, bottom = '', '', ''
    has_type, has_top = False, False
    for i in inp:
        if not has_type:
            if not i.startswith('"'):
                meme_type += i + ' '
            else:
                has_type = True
        if not has_top and has_type:
            top += i + ' '
            if i.endswith('"'):
                has_top = True
        elif has_top and has_type:
            bottom += i + ' '
    meme_type, top, bottom = meme_type.rstrip(' '), top.rstrip(' '), bottom.rstrip(' ')
    top, bottom = re.sub('"', '', top), re.sub('"', '', bottom)
    data = {
            "meme":meme_type,
            "top":top,
            "bottom":bottom
            }
    data = urllib.parse.urlencode(data)
    rqst = urllib.request.urlopen(URL + data)
    data = rqst.read()
    img = open(f, 'wb')
    img.write(data)
    img.close()
    return f


def get_help():
    return '\n/meme [meme] ["Top Text"] ["Bottom Text"]: Erstellt eine Meme(Alle Memes http://apimeme.com/)'


if __name__ == '__main__':
    print(get_meme(['City', 'Bear', '"Top', 'Text"', '"Bottom', 'Text"']))
