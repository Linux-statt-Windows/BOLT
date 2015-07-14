#!/bin/env python3

import re

class module_wrapper(object):

    def __init__(self, inmodules):
        self.modules = inmodules
        self.loaded_modules, self.methods = [],[]
        for mod in inmodules:
            if inmodules[mod] == 'True':
                self.loaded_modules.append(__import__(mod,globals(),locals(),['callback',],1))
        for mod in self.loaded_modules:
            self.methods.append(getattr(mod,'callback'))
        self.plugs = []
        for method in self.methods:
            self.plugs.append(method())
        self.plugins = dict(self.plugs)


    def get_response(self, cmd):
        cmd = re.sub('@.*', '', cmd)
        if cmd in self.plugins:
            return self.plugins[cmd](self.rm_command(cmd))
    

    def get_help(self):
        help = 'Diese Befehle verstehe ich ;)\n'
        for i in self.modules:
            if self.modules[i] == 'True':
                if i == 'fb':
                    help += '\n/lsw Facebook: Bekomme die Links zu unserer Facebook Gruppe und Seite.'
                elif i == 'themadesmonats':
                    help += '\n/lsw Thema: Finde heraus, was das aktuelle thema des Monats ist.'
                elif i == 'distrodesmonats':
                    help += '\n/lsw Distro: Finde heraus, welches die aktuelle Distro des Monats ist.'
                elif i == 'mumble':
                    help += '\n/lsw Mumble: Bekomme Infos über unsereren Mumble Server.'
                elif i == 'nine_gag':
                    help += '\n/9gag - sendet ein zufälliges 9gag Meme'
                elif i == 'forum':
                    help += '\n/lsw: Bekomme den Link zu unserer Homepage.'
                elif i == 'calc':
                    help += '\n/calc [Term] - Rechnet den Term aus(kein Punkt-vor-Strich/keine Klammern)'
                elif i == 'faq':
                    help += '\n/lsw FAQ: Siehe unsere Antworten auf beliebte Fragen.'
                elif i == 'Version':
                    help += '\n/lsw Version: Bekomme Infos über das Plugin selbst.'
                elif i == 'google':
                    help += '\n/google [suchbegriff]: Zeigt die  ersten Suchergebnisse der Google-Suche'
        return help

    def rm_command(self, inp):
        exp = re.sub('\/[a-zA-Z]*\s', '', inp)
        return exp

