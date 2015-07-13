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
import math
import random
from html.parser import HTMLParser

BASE_URL=''
GROUP_ID=''
TOKEN=''

SAVE_FILE='/var/lib/bolt/update_id.data'
CONFIG_FILE='/etc/bolt'

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


def get_updates(url):
    while True:
        data = 'limit=100&offset=' + get_latest_update_id() 
        rqst = urllib.request.urlopen(url, data.encode('utf-8'))
        data = json.loads(rqst.read().decode('utf-8'))
        for msg in data['result']:
            if str(msg['message']['chat']['id']) == GROUP_ID:
                if 'text' in msg['message']:
                    if check_update_id(msg['update_id']):
                        cmd = msg['message']['text']
                        if cmd.startswith('/'):
                            #TODO: Implement features and commands
                            if cmd.startswith('/hilfe'):
                                send_message('Diese Kommandos verstehe ich :)\n\n/hilfe - diese Hilfe')
                            elif cmd.startswith('/calc'):
                                send_message(calc(rm_command(cmd)))
                            elif cmd.startswith('/9gag'):
                                nine_gag()
        time.sleep(INTERVAL)


def nine_gag():
    url = 'http://api-9gag.herokuapp.com/'
    rqst = urllib.request.urlopen('http://9gag.com/random')
    data = rqst.read().decode('utf-8')
    parser = nine_gag_parser()
    parser.feed(data)
    img_url = parser.img_url
    title = parser.data
    if title and img_url:
        send_message(title + '\n\n' + img_url)
        parser.fetched = False


def calc(inp):
    inp = re.sub('\s', '', inp)
    exp = re.split('[\+\-\*\/%\^]', inp)
    inp = re.sub('^' + exp[0], '', inp)
    if len(exp) == 1:
        l = 2
    else:
        l = len(exp) - 1
    for i in range(l):
        if inp.startswith('+'):
            inp = re.sub('^'+'\+'+str(exp[i+1]), '', inp)
            exp[i+1] = (float(exp[i]) + float(exp[i+1]))
        elif inp.startswith('-'):
            inp = re.sub('^'+'\-'+str(exp[i+1]), '', inp)
            exp[i+1] = (float(exp[i]) - float(exp[i+1]))
        elif inp.startswith('*'):
            inp = re.sub('^'+'\*'+str(exp[i+1]), '', inp)
            exp[i+1] = (float(exp[i]) * float(exp[i+1]))
        elif inp.startswith('/'):
            if exp[i+1] == '0':
                return 'Nope :P'
            else:
                inp = re.sub('^'+'\/'+str(exp[i+1]), '', inp)
                exp[i+1] = (float(exp[i]) / float(exp[i+1]))
        elif inp.startswith('^'):
            inp = re.sub('^'+'\^'+str(exp[i+1]), '', inp)
            exp[i+1] = (float(exp[i]) ** float(exp[i+1]))
        elif inp.startswith('%'):
            exp[i+1] = (float(exp[i]) % int(exp[i+1]))
        elif inp.startswith('sqrt'):
            exp = re.sub('\\)', '', re.sub('sqrt\(', '', inp))
            return str(math.sqrt(float(exp)))
        else:
            return 'Falscher Befehl'
    return exp[len(exp)-1]


def rm_command(inp):
    exp = re.sub('\/[a-zA-Z]*\s', '', inp)
    return exp


def send_message(msg):
    msg = 'chat_id=' + GROUP_ID + '&text=' + str(msg)
    rqst = urllib.request.urlopen(BASE_URL + 'sendMessage', msg.encode('utf-8'))

    #NOTE: Maybe send check?
    #data = json.loads(rqst.read().decode('utf-8'))


def send_image(url):
    print(url)
    msg = 'chat_id=' + GROUP_ID + '&photo=' + url
    rqst = urllib.request.urlopen(BASE_URL + 'sendPhoto', msg.encode('utf-8'))


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
    group_id, token, interval = '', '', ''
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
    
    get_updates(BASE_URL + 'getUpdates')


if __name__ == '__main__':
    main()
