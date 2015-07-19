#!/bin/env python3

import urllib.request
import json
import random
from html.parser import HTMLParser
import re

URL = 'http://www.daujones.com/detail.php?usrid='


class dau_parser(HTMLParser):

    def __init__(self):
        super().__init__()
        self.is_story = False
        self.tag = None
        self.is_title = False
        self.title = None
        self.is_data = False
        self.is_content = False

    def handle_starttag(self, tag, attrs):
        self.tag = tag
        if tag == 'h2':
            if attrs[0][1] == 'center':
                self.is_title = True


    def handle_data(self, data):
        if self.is_title:
            self.is_title = False
            self.title = data


class MLStripper(HTMLParser):

    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs = True
        self.fed =  []

    def handle_data(self, data):
        self.fed.append(data)

    def get_data(self):
        return ''.join(self.fed)


def callback():
    return '/daujones', get_dau


def get_dau(inp):
    parser = dau_parser()
    stripper = MLStripper()
    while not parser.is_story:
        num = random.randint(0,10853)
        rqst = urllib.request.urlopen(URL + str(num))
        data = rqst.read().decode('iso-8859-1')
        parser.feed(data)
        if parser.title is not None:
            parser.is_story = True
    data = re.split('<\/span><\/center>', data)
    data = re.split('<span style', data[1])
    stripper.feed(data[0])
    return parser.title \
            + '\n\n' + stripper.get_data()


def get_help():
    return '\n/daujones: Zeigt eine zufällige DAU Geschichte'


if __name__ == '__main__':
    print(get_dau(0))
