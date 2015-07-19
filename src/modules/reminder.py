#!/bin/env python3

import urllib.request
import json

URL = ''

def callback():
    return '', get_reminder


def get_reminder(inp):
    # TODO:
    #  - parse json api
    #  - logic for event handling
    return 'data'


def get_help():
    return ''


def get_repeat():
    return 1


if __name__ == '__main__':
    print(get_reminder(0))
