#!/bin/env python3

import re
import math

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


if __name__ == '__main__':
    inp = input('Input-String: ')
    calc(inp)
