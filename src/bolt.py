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

BASE_URL=''
GROUP_ID=0
TOKEN=''

SAVE_FILE='/var/lib/telegroup-admin-helper/update_id.data'
CONFIG_FILE='/etc/bolt'

def get_updates(url):
    old_update_id = 0
    while True:
        rqst = urllib.request.urlopen(url)
        data = json.loads(rqst.read().decode('utf-8'))
        print(data)
        time.sleep(INTERVAL)


def parse_config():
    notify_id, group_id, token, banned_nicks, interval = '', '', '', [''], ''
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
        return group_id, token, interval


def main():
    # parse config
    global GROUP_ID
    global TOKEN
    global INTERVAL
    group_id, token, interval = parse_config()
    if group_id is not '' and token is not '' and interval is not '':
        GROUP_ID = int(group_id)
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
    if not os.path.isdir('/var/lib/telegroup-admin-helper'):
        os.mkdir('/var/lib/telegroup-admin-helper')

    print('Starting BOLT...')
    global BASE_URL
    BASE_URL = 'https://api.telegram.org/bot' + TOKEN + '/' # base url for bots (DON'T CHANGE!)
    
    print(BASE_URL)

    get_updates(BASE_URL + 'getUpdates')


if __name__ == '__main__':
    main()
