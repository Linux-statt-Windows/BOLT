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

    def handle_starttag(self, tag, attrs):
        self.tag = tag
        if tag == 'link':
            if attrs[0][1] == 'image_src':
                self.img_url = attrs[1][1]

    def handle_data(self, data):
        data = re.sub('\n*', '', data)
        data = re.sub(' - 9GAG', '', data)
        if self.tag == 'title' and len(data) > 0 and not self.fetched:
            self.data = data
            self.fetched = True


def get_meme():
    rqst = urllib.request.urlopen('http://9gag.com/random')
    data = rqst.read().decode('utf-8')
    parser = nine_gag_parser()
    parser.feed(data)
    img_url = parser.img_url
    title = parser.data
    if title and img_url:
        return (title + '\n\n' + img_url)
        #parser.fetched = False


if __name__ == '__main__':
    get_meme()
