#!/bin/env python3
#
# BOLT
#
# © 2015 LsW Community
# Licensed under the GNU General Public License

import argparse
import glob
import http.client
import json
import os
import re
import sys
import time
import urllib.request
from threading import Thread

import multipart
from modules.wrapper import *

class BOLT(Thread):

    def __init__(self, url, modules, repeat_events, interval, group_id, banned_nicks, notify_id):
        super().__init__()
        self.url = url
        self.modules = modules
        self.repeat_events = repeat_events
        self.interval = interval
        self.group_id = group_id
        self.banned_nicks = banned_nicks
        self.notify_id = notify_id
        self.save_file = '/var/lib/bolt/' + str(group_id)

    def run(self):
        r = []
        for event in self.repeat_events:
            event = (self.convert_sec(event[0]), event[1])
            r.append(list(event + (0,)))

        while True:
            # Repeatable events
            for event in r:
                t = time.time()
                if event[2] + event[0] <= t:
                    response = event[1](0)
                    if response != None:
                        if response.startswith('/'):
                            if os.path.exists(response):
                                self.send_image(response)
                            else:
                                self.send_message('Fehler beim Senden der Antwort')
                        else:
                            self.send_message(response)
                    event[2] = int(t)
            data = 'limit=300&offset=' + str(self.get_latest_update_id())
            rqst = urllib.request.urlopen(self.url + 'getUpdates', data.encode('utf-8'))
            try:
                data = json.loads(rqst.read().decode('utf-8'))
                #print(data)
            except Exception as e:
                print ( "Some Exception occured while fetching data from telegram server:\n" + e )
            # React to commands
            for msg in data['result']:
                if str(msg['message']['chat']['id']) == self.group_id:
                    if 'text' in msg['message']:
                        if self.check_update_id(msg['update_id']):
                            cmd = msg['message']['text']
                            if cmd.startswith('/'):
                                response = str(self.modules.get_response(cmd))
                                if response.startswith('/'):
                                    if os.path.exists(response):
                                        self.send_image(response)
                                    else:
                                        self.send_message('Fehler beim Senden der Antwort')
                                else:
                                    self.send_message(response)

            # Check for banned nicks
            for msg in data['result']:
                if 'new_chat_participant' in msg['message']:
                    if msg['message']['new_chat_participant']['username'] in self.banned_nicks:
                        if self.check_update_id(msg['update_id']):
                            self.send_notification('WARNNUNG! Der verbannte Username ' + msg['message']['new_chat_participant']['username'] + ' hat die Gruppe wieder betreten!')

            time.sleep(self.interval)


    def convert_sec(self, inp):
        if inp == 'weekly':
            return 604800
        elif inp == 'biweekly':
            return 604800*2
        elif inp == 'daily':
            return 86400
        elif inp == 'monthly':
            return 2592000
        elif inp == 'hourly':
            return 3600
        else:
            return inp


    def rm_command(self, inp):
        exp = re.sub('\/[a-zA-Z]*\s', '', inp)
        return exp


    # Reporting banned user
    def send_notification(self, msg):
        print(self.notify_id)
        if msg:
            msg = re.sub('&', '%26', str(msg))
            msg = 'chat_id=' + self.notify_id + '&text=' + str(msg)
            rqst = urllib.request.urlopen(self.url + 'sendMessage', msg.encode('utf-8'))

            #NOTE: Maybe send check?
            #data = json.loads(rqst.read().decode('utf-8'))


    # Answering to commands
    def send_message(self, msg):
        if msg:
            msg = re.sub('&', '%26', str(msg))
            msg = 'chat_id=' + self.group_id + '&text=' + str(msg)
            rqst = urllib.request.urlopen(self.url + 'sendMessage', msg.encode('utf-8'))

            #NOTE: Maybe send check?
            #data = json.loads(rqst.read().decode('utf-8'))


    def send_image(self, filename):
        files = [('photo', 'image.jpg', filename)]
        params =  [('chat_id', self.group_id)]

        # Build multipart/form data
        parts = urllib.parse.urlparse(self.url + 'sendPhoto')
        scheme = parts[0]
        host = parts[1]
        selector = parts[2]
        content_type, body = multipart.encode_multipart(files, params)

        # Send multipart/form data
        if scheme == 'http':
            host = http.client.HTTPConnection(host)
        elif scheme == 'https':
            host = http.client.HTTPSConnection(host)
        host.request('POST', self.url + 'sendPhoto', body=body, headers={'content-type':content_type, 'content-length':str(len(body))})
        host.getresponse()


    def check_update_id(self, new_id):
        new_id = str(new_id)
        if os.path.isfile(self.save_file):
            f = open(self.save_file, 'r')
            line = f.readline()
            f.close()
            old_id = line
        else:
            old_id = '0'
        if new_id > old_id:
            f = open(self.save_file, 'w+')
            f.write(new_id)
            f.close()
            return True
        else:
            return False


    def get_latest_update_id(self):
        if os.path.isfile(self.save_file):
            f = open(self.save_file, 'r')
            line = f.readline()
            f.close()
            return line
        return 0


def parse_config(config_file):
    group_id, token, interval, modules, banned_nicks, notify_id = '', '', '', '', '', ''
    if os.path.isfile(config_file):
        f = open(config_file, 'r')
        line = f.readlines()
        for i in range(len(line)):
            if not line[i].startswith('#') and not line[i].startswith('\n'):
                if line[i].startswith('GROUP_ID'):
                    group_id = re.sub('\n', '', re.sub('GROUP_ID=','', line[i]))
                elif line[i].startswith('TOKEN'):
                    token = re.sub('\n', '', re.sub('TOKEN=','', line[i]))
                elif line[i].startswith('INTERVAL'):
                    interval = re.sub('\n', '', re.sub('INTERVAL=','', line[i]))
                elif line[i].startswith('NOTIFY_ID'):
                    notify_id = re.sub('\n', '', re.sub('NOTIFY_ID=','', line[i]))
                elif line[i].startswith('BANNED_NICKS'):
                    banned_nicks = re.sub('\n', '', re.sub('BANNED_NICKS=', '', line[i]))
                    banned_nicks = re.sub('\'\]', '', re.sub('\[\'', '', banned_nicks))
                    banned_nicks = re.sub('\s*', '', banned_nicks)
                    banned_nicks = re.split('\',\'', banned_nicks)
                elif line[i].startswith('{'):
                    for j in range(len(line)-i):
                        if line[i+j] == '}':
                            break
                        else:
                            modules += line[i+j]
                    break
        return group_id, token, interval, modules, banned_nicks, notify_id


def get_configs():
    return None


def main():
    # arg parsing
    parser = argparse.ArgumentParser()
    parser.add_argument('-b', '--background', action='store_true', help='starts bot in background')

    args = parser.parse_args()

    print('Starting BOLT...')

    if args.background:
        fpid = os.fork()
        if fpid != 0:
            sys.exit(0)

    # check if data path exists
    if not os.path.isdir('/var/lib/bolt'):
        os.mkdir('/var/lib/bolt')

    # get config files
    config_files = glob.glob('/etc/channel.d/*')

    for f in config_files:
        # parse config
        group_id, token, interval, modules, banned_nicks, notify_id = parse_config(f)
        if group_id is not '' and token is not '' and interval is not '' and modules is not '':
            modules = json.loads(modules)
        else:
            print('ERROR: Please set your config correctly!')
            return

        modules = module_wrapper(modules)
        repeat_events = modules.get_repeat_events()

        bot = BOLT('https://api.telegram.org/bot' + token + '/', modules, repeat_events, float(interval), group_id, banned_nicks, notify_id)
        bot.start()


if __name__ == '__main__':
    main()
