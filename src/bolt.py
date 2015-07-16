#!/bin/env python3
#
# BOLT
#
# © 2015 LsW Community
# Licensed under the GNU General Public License

import os
import urllib.request
import json
import argparse
import time
import re
import sys
import http.client

from modules.wrapper import *
import multipart

BASE_URL=''
GROUP_ID=''
TOKEN=''
MODULES=['']

SAVE_FILE='/var/lib/bolt/update_id.data'
CONFIG_FILE='/etc/bolt'


def get_updates(url, modules):
    while True:
        data = 'limit=3&offset=' + str(get_latest_update_id())
        rqst = urllib.request.urlopen(url, data.encode('utf-8'))
        data = json.loads(rqst.read().decode('utf-8'))
        for msg in data['result']:
            if str(msg['message']['chat']['id']) == GROUP_ID:
                if 'text' in msg['message']:
                    if check_update_id(msg['update_id']):
                        cmd = msg['message']['text']
                        response = modules.get_response(cmd)
                        if os.path.exists(response):
                            send_image(response)
                        else:
                            send_message(response)
        time.sleep(INTERVAL)


def rm_command(inp):
    exp = re.sub('\/[a-zA-Z]*\s', '', inp)
    return exp


def send_message(msg):
    if msg:
        msg = re.sub('&', '%26', str(msg))
        msg = 'chat_id=' + GROUP_ID + '&text=' + str(msg)
        rqst = urllib.request.urlopen(BASE_URL + 'sendMessage', msg.encode('utf-8'))

        #NOTE: Maybe send check?
        #data = json.loads(rqst.read().decode('utf-8'))


def send_image(filename):
    files = [('photo', 'image.jpg', filename)]
    params =  [('chat_id',GROUP_ID)]
    parts = urllib.parse.urlparse(BASE_URL + 'sendPhoto')
    scheme = parts[0]
    host = parts[1]
    selector = parts[2]                 
    content_type, body = multipart.encode_multipart(files, params)
    if scheme == 'http':
        host = http.client.HTTPConnection(host)
    elif scheme == 'https':
        host = http.client.HTTPSConnection(host)
    host.request('POST', BASE_URL + 'sendPhoto', body=body, headers={'content-type':content_type, 'content-length':str(len(body))})


def check_update_id(new_id):
    new_id = str(new_id)
    if os.path.isfile(SAVE_FILE):
        f = open(SAVE_FILE, 'r')
        line = f.readline()
        f.close()
        old_id = line
    else:
        old_id = '0'
    if new_id > old_id:
        f = open(SAVE_FILE, 'w+')
        f.write(new_id)
        f.close()
        return True
    else:
        return False


def get_latest_update_id():
    if os.path.isfile(SAVE_FILE):
        f = open(SAVE_FILE, 'r')
        line = f.readline()
        f.close()
        return line
    return 0


def parse_config():
    group_id, token, interval, modules = '', '', '', ''
    if os.path.isfile(CONFIG_FILE):
        f = open(CONFIG_FILE, 'r')
        line = f.readlines()
        for i in range(len(line)):
            if not line[i].startswith('#') and not line[i].startswith('\n'):
                if line[i].startswith('GROUP_ID'):
                    group_id = re.sub('\n', '', re.sub('GROUP_ID=','', line[i]))
                elif line[i].startswith('TOKEN'):
                    token = re.sub('\n', '', re.sub('TOKEN=','', line[i]))
                elif line[i].startswith('INTERVAL'):
                    interval = re.sub('\n', '', re.sub('INTERVAL=','', line[i]))
                elif line[i].startswith('{'):
                    for j in range(len(line)-i):
                        if line[i+j] == '}':
                            break
                        else:
                            modules += line[i+j]
                    break
        return group_id, token, interval, modules


def main():
    # parse config
    global GROUP_ID
    global TOKEN
    global INTERVAL
    global MODULES
    group_id, token, interval, modules = parse_config()
    if group_id is not '' and token is not '' and interval is not '' and modules is not '':
        modules = json.loads(modules)
        MODULES = modules
        GROUP_ID = group_id
        TOKEN = token
        INTERVAL = float(interval)
    else:
        print('ERROR: Please set your config correctly!')
        return

    # arg parsing
    parser = argparse.ArgumentParser()
    parser.add_argument('--token', type=str, help='token of your bot')
    parser.add_argument('--interval', type=int, help='interval between two updates')
    parser.add_argument('--group-id', type=str, help='ID of your telegram-group')

    args = parser.parse_args()

    if args.token:
        TOKEN = args.token
    if args.group_id:
        GROUP_ID = args.group_id
    if args.interval:
        INTERVAL = args.interval

    # check if data path exists
    if not os.path.isdir('/var/lib/bolt'):
        os.mkdir('/var/lib/bolt')

    print('Starting BOLT...')
    global BASE_URL
    BASE_URL = 'https://api.telegram.org/bot' + TOKEN + '/' # base url for bots (DON'T CHANGE!)
    
    modules = module_wrapper(MODULES)

    get_updates(BASE_URL + 'getUpdates', modules)


if __name__ == '__main__':
    main()
