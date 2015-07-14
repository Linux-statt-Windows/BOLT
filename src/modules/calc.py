#!/bin/env python3

import re
import math

def callback():
    return '/calc', calc


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
            exp[i+1] = float(exp[i]) + float(exp[i+1])
        elif inp.startswith('-'):
            inp = re.sub('^'+'\-'+str(exp[i+1]), '', inp)
            exp[i+1] = float(exp[i]) - float(exp[i+1])
        elif inp.startswith('*'):
            inp = re.sub('^'+'\*'+str(exp[i+1]), '', inp)
            exp[i+1] = float(exp[i]) * float(exp[i+1])
        elif inp.startswith('/'):
            if exp[i+1] == '0':
                return 'Nope :P'
            else:
                inp = re.sub('^'+'\/'+str(exp[i+1]), '', inp)
                exp[i+1] = float(exp[i]) / float(exp[i+1])
        elif inp.startswith('^'):
            inp = re.sub('^'+'\^'+str(exp[i+1]), '', inp)
            if int(exp[i+1]) <= 512:
                exp[i+1] = float(exp[i]) ** float(exp[i+1])
            else:
                return 'Zahl zu groß'
        elif inp.startswith('%'):
            exp[i+1] = float(exp[i]) % int(exp[i+1])
        elif inp.startswith('sqrt'):
            exp = re.sub('\\)', '', re.sub('sqrt\(', '', inp))
            return str(math.sqrt(float(exp)))
        else:
            return 'Falscher Befehl'
    return exp[len(exp)-1]


def get_help():
    return '\n/calc [Term] - Rechnet den Term aus(kein Punkt-vor-Strich/keine Klammern)'


if __name__ == '__main__':
    inp = input('Input-String: ')
    calc(inp)
