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

# own modules
import modules.themadesmonats as themadesmonats
import modules.distrodesmonats as distrodesmonats
import modules.nine_gag as nine_gag
import modules.calc as calc
import modules.faq as faq
import modules.forum as forum
import modules.fb as fb
import modules.mumble as mumble
import modules.github as github

BASE_URL=''
GROUP_ID=''
TOKEN=''
MODULES=['']

SAVE_FILE='/var/lib/bolt/update_id.data'
CONFIG_FILE='/etc/bolt'


def get_updates(url):
    while True:
        data = 'limit=3&offset=' + str(get_latest_update_id())
        rqst = urllib.request.urlopen(url, data.encode('utf-8'))
        data = json.loads(rqst.read().decode('utf-8'))
        for msg in data['result']:
            if str(msg['message']['chat']['id']) == GROUP_ID:
                if 'text' in msg['message']:
                    if check_update_id(msg['update_id']):
                        cmd = msg['message']['text']
                        #TODO: Implement features and commands
                        if cmd.startswith('/hilfe'):
                            send_message('Diese Kommandos verstehe ich :)\n\n' \
                                    + '/hilfe - diese Hilfe\n' \
                                    + '/calc [Term] - Rechnet den Term aus(kein Punkt-vor-Strich/keine Klammern)\n' \
                                    + '/9gag - sendet ein zufälliges 9gag Meme\n' \
                                    + '/lsw - Plugin der Linux statt Windows Community')
                        elif cmd.startswith('/calc') and MODULES['calc']:
                            send_message(calc.calc(rm_command(cmd)))
                        elif cmd.startswith('/9gag') and MODULES['9gag']:
                            send_message(nine_gag.get_meme())
                        elif cmd == '/lsw' and MODULES['Forum']:
                            name, short_url, long_url, de_url, eu_url, faq_url, rules_url = forum.get_forum()
                            send_message(name\
                                    + '\n\nShort URL: ' + short_url \
                                    + '\nLong URL: ' + long_url \
                                    + '\nDE URL: ' + de_url \
                                    + '\nEU URL:' + eu_url \
                                    + '\nFAQ: ' + faq_url \
                                    + '\nRegeln: ' + rules_url)
                        elif cmd.startswith('/lsw'):
                            cmd = re.sub('/lsw ', '', cmd)
                            if cmd.startswith('Thema') and MODULES['Thema']:
                                name, month, in_url = themadesmonats.monthly_topic()
                                send_message(name\
                                        + '\n\nMonat: ' + month \
                                        + '\nURL: ' + in_url)
                            elif cmd.startswith('Distro') and MODULES['Distro']:
                                name, month, in_url = distrodesmonats.get_distro()
                                send_message(name\
                                        + '\n\nMonat: ' + month \
                                        + '\nURL: ' + in_url)
                            elif cmd.startswith('FAQ') and MODULES['FAQ']:
                                name, in_url = faq.get_faq()
                                send_message(name \
                                        + '\n\nURL: ' + in_url)
                            elif cmd.startswith('Facebook') and MODULES['Facebook']:
                                group_url, short_url, site_url = fb.get_fb()
                                send_message('Facebook Gruppen' \
                                        + '\n\nGruppe: ' + group_url \
                                        + '\nGruppe(short URL): ' + short_url \
                                        + '\nFacebook-Seite: ' + site_url)
                            elif cmd.startswith('Mumble') and MODULES['Mumble']:
                                direct_url, in_url, port = mumble.get_mumble()
                                send_message('Mumble\n\n' \
                                        + 'Direct Link: ' + direct_url \
                                        + '\nURL: ' + in_url \
                                        + '\nPort: ' + str(port))
                            elif cmd.startswith('Github') and MODULES['Github']:
                                in_url, short_url = github.get_github()
                                send_message('Github' \
                                        + '\n\nURL: ' + in_url \
                                        + '\nShort URL: ' + short_url)
                            elif cmd.startswith('Version') and MODULES['Version']:
                                send_message('LsW-Plugins' \
                                        + '\n\n/lsw: Bekomme den Link zu unserer Homepage.'
                                        + '\n/lsw Thema: Finde heraus, was das aktuelle Thema des Monats ist.' \
                                        + '\n/lsw Distro: Finde heraus, welches die aktuelle Distro des Monats ist.' \
                                        + '\n/lsw Mumble: Bekomme Infos über unsereren Mumble Server.' \
                                        + '\n/lsw FAQ: Siehe unsere Antworten auf beliebte Fragen.' \
                                        + '\n/lsw Facebook: Bekomme die Links zu unserer Facebook Gruppe und Seite.' \
                                        + '\n/lsw Version: Bekomme Infos über das Plugin selbst.')
                            elif not cmd.startswith(''):
                                a = 1
                        elif cmd.startswith('/'):
                            send_message('Ungültiger Befehl! Diese Kommandos verstehe ich :)\n\n' \
                                    + '/hilfe - diese Hilfe\n' \
                                    + '/calc [Term] - Rechnet den Term aus(kein Punkt-vor-Strich/keine Klammern)\n' \
                                    + '/9gag - sendet ein zufälliges 9gag Meme\n' \
                                    + '/lsw - Plugin der Linux statt Windows Community')
        time.sleep(INTERVAL)


def rm_command(inp):
    exp = re.sub('\/[a-zA-Z]*\s', '', inp)
    return exp


def send_message(msg):
    msg = re.sub('&', '%26', str(msg))
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
    
    get_updates(BASE_URL + 'getUpdates')


if __name__ == '__main__':
    main()
