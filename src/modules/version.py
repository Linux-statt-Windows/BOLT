#!/bin/env python3

import urllib.request
import json

URL = ''

def callback():
    return '/lsw Version', get_version


def get_version(inp):
    return 'LsW-Plugins' \
                + '\n\n/lsw: Bekomme den Link zu unserer Homepage.' \
                + '\n/lsw Thema: Finde heraus, was das aktuelle thema des Monats ist.' \
                + '\n/lsw Distro: Finde heraus, welches die aktuelle Distro des Monats ist.' \
                + '\n/lsw Mumble: Bekomme Infos über unsereren Mumble Server.' \
                + '\n/lsw FAQ: Siehe unsere Antworten auf beliebte Fragen.' \
                + '\n/lsw Facebook: Bekomme die Links zu unserer Facebook Gruppe und Seite.' \
                + '\n/lsw Version: Bekomme Infos über das Plugin selbst.'
                   


if __name__ == '__main__':
    print(get_())
