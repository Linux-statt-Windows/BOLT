#!/bin/env python3

import urllib.request
from html.parser import HTMLParser
import re

class nine_gag_parser(HTMLParser):

    def __init__(self):
        super().__init__()
        self.img_url = None
        self.tag = None
        self.data = None
        self.fetched = False
        self.is_gif = True

    def handle_starttag(self, tag, attrs):
        self.tag = tag
        if tag == 'link':
            if attrs[0][1] == 'image_src':
                self.img_url = attrs[1][1]
        if tag == 'div':
            if len(attrs) >= 2:
                if attrs[1][0] == 'data-image':
                    self.is_gif = True

    def handle_data(self, data):
        data = re.sub('\n*', '', data)
        data = re.sub(' - 9GAG', '', data)
        if self.tag == 'title' and len(data) > 0 and not self.fetched:
            self.data = data
            self.fetched = True


def callback():
    return '/9gag', get_meme


def get_meme(inp):
    parser = nine_gag_parser()
    while parser.is_gif:
        parser.is_gif = False
        rqst = urllib.request.urlopen('http://9gag.com/random')
        data = rqst.read().decode('utf-8')
        parser.feed(data)
        img_url = parser.img_url
        title = parser.data
        if title and img_url and not parser.is_gif:
            return (title + '\n\n' + img_url)


def get_help():
    return '\n/9gag - sendet ein zufälliges 9gag Meme'


if __name__ == '__main__':
    print(get_meme(0))
