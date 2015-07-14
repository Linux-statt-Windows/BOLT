#!/bin/env python3

import re

class module_wrapper(object):

    def __init__(self, inmodules):
        self.modules = inmodules
        self.loaded_modules, self.methods, self.helps = [],[],[]
        for mod in inmodules:
            if inmodules[mod] == 'True':
                self.loaded_modules.append(__import__(mod,globals(),locals(),['callback',],1))
        for mod in self.loaded_modules:
            self.methods.append(getattr(mod,'callback'))
            self.helps.append(getattr(mod, 'get_help'))
        self.plugs = []
        for method in self.methods:
            self.plugs.append(method())
        self.plugins = dict(self.plugs)


    def get_response(self, cmd):
        cmd = re.sub('@.*', '', cmd)
        if cmd.startswith('/hilfe'):
            return self.get_help()
        elif cmd in self.plugins:
            return self.plugins[cmd](self.rm_command(cmd))
        else:
            cmd = re.split(' ',cmd)
            if cmd[0] in self.plugins:
                new_cmd = []
                for c in range(1,len(cmd)):
                    new_cmd.append(cmd[c])
                return self.plugins[cmd[0]](new_cmd)


    def get_help(self):
        help = 'Diese Befehle verstehe ich ;)\n'
        for h in self.helps:
            help += h()
        return help

    def rm_command(self, inp):
        exp = re.sub('\/[a-zA-Z]*\s', '', inp)
        return exp

