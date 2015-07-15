#!/bin/env python3

import urllib.request
import json

URL = 'https://hacker-news.firebaseio.com/v0/topstories.json'

def callback():
    return '/hackernews', get_hackernews


def get_hackernews(inp):
    rqst = urllib.request.urlopen(URL)
    data = json.loads(rqst.read().decode('utf-8'))
    news = []
    for i in range(5):
        rqst = urllib.request.urlopen('https://hacker-news.firebaseio.com/v0/item/' + str(data[i]) + '.json')
        news.append(json.loads(rqst.read().decode('utf-8')))
    data = 'Hacker-News\n'
    for new in news:
        data += '\nTitel: ' + new['title'] \
                + '\nURL: ' + new['url'] + '\n'
    return data


def get_help():
    return '\n/hackernews: Get the latest hacker news'


if __name__ == '__main__':
    print(get_hackernews(0))
