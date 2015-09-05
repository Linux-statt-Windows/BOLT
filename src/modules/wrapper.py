#!/bin/env python3

import re
import urllib.request

class module_wrapper(object):

    def __init__(self, inmodules):
        self.modules = inmodules
        self.loaded_modules, self.methods, self.helps = [],[],[]
        for mod in inmodules:
            if inmodules[mod] == 'True':
                self.loaded_modules.append(__import__(mod,globals(),locals(),['callback',],1))
        self.repeat_modules = []
        for mod in self.loaded_modules:
            if 'get_repeat' in dir(mod):
                interval = getattr(mod, 'get_repeat')()
                tpl = (interval, getattr(mod, 'callback')()[1])
                self.repeat_modules.append(tpl)
            self.methods.append(getattr(mod,'callback'))
            self.helps.append(getattr(mod, 'get_help')())
        self.plugs = []
        self.helps = sorted(self.helps)
        for method in self.methods:
            self.plugs.append(method())
        self.plugins = dict(self.plugs)


    def get_repeat_events(self):
        return self.repeat_modules


    def get_response(self, cmd):
        cmd = re.sub('@.*', '', cmd)
        try:
            if cmd.startswith('/'):
                if cmd.lower().startswith('/hilfe'):
                    if len(cmd) > 7:
                        return self.get_help(cmd[7:])
                    else:
                        return self.get_help(None)
                elif cmd.lower() in self.plugins:
                    return self.plugins[cmd.lower()](self.rm_command(cmd))
                else:
                    cmd = re.split(' ',cmd)
                    if cmd[0].lower() in self.plugins:
                        new_cmd = [cmd[i] for i in range(1, len(cmd))]
                        return self.plugins[cmd[0].lower()](new_cmd)
                    else:
                        #rqst = urllib.request.urlopen('http://apimeme.com/meme?meme=Grandma+Finds+The+Internet&top=Wat+willst&bottom=du+von+mir%3F')
                        rqst = urllib.request.urlopen('http://m.memegen.com/w5td5q.jpg')
                        data = rqst.read()
                        img = open('/var/lib/bolt/error.png', 'wb')
                        img.write(data)
                        img.close()
                        return '/var/lib/bolt/error.png'
        except:
            return 'Fehler im gewünschten Plugin'


    def get_help(self, cmd):
        help = 'Diese Befehle verstehe ich ;)\n'
        for h in self.helps:
            if cmd is not None:
                if h.lstrip('\n/').startswith(cmd):
                    return h
            else:
                help += h
        return help

    def rm_command(self, inp):
        exp = re.sub('\/[a-zA-Z]*\s', '', inp)
        return exp

