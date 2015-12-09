#!/bin/env python3

import urllib.request
import json

URL_SCAN = 'https://api.shodan.io/shodan/host/'
URL_EXPLOIT = 'https://exploits.shodan.io/api/search?query='

API_KEY = ''

def callback():
    return '/shodan', get_shodan


def get_shodan(cmd):
    if len(cmd) < 2:
        return 'Ein Fehler ist aufgetreten. Bitte überprüfe deine Suche'
    if cmd[0] == 'exploit':
        try:
            rqst = urllib.request.urlopen(URL_EXPLOIT + str(cmd[1]) + '&key=' + API_KEY)
            data = json.loads(rqst.read().decode('utf-8'))['matches'][0]
        except Exception as e:
            return 'Ein Fehler ist aufgetreten. Bitte überprüfe deine Suche'
        rsp = 'Suchbegriff: ' + cmd[1] + '\n\n'
        rsp += 'CVE: ' + str(data['cve'][0]) + '\n'
        rsp += 'Beschreibung: ' + str(data['description']) + '\n'
        return rsp
    elif cmd[0] == 'scan':
        try:
            rqst = urllib.request.urlopen(URL_SCAN + str(cmd[1]) + '?key=' + API_KEY)
            data = json.loads(rqst.read().decode('utf-8'))
        except Exception as e:
            return 'Ein Fehler ist aufgetreten. Bitte überprüfe deine Suche'
        rsp = 'IP: ' + cmd[1] + '\n'
        if 'vulns' in data:
            rsp += 'Verwundbarkeiten: ' + str(data['vulns'])  + '\n'
        rsp += 'Ports: ' + str(data['ports']) + '\n'
        rsp += 'Stadt: ' + str(data['city']) + '\n'
        rsp += 'Land: ' + str(data['country_name']) + '\n'
        rsp += 'ISP: ' + str(data['isp']) + '\n'
        return rsp


def get_help():
    return '\n/shodan: exploit [cve] - sucht nach einem Exploit\n\tscan [ip] - sucht Daten zur gegebenen IP heraus'


if __name__ == '__main__':
    print()
