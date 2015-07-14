#!/bin/env python3

import re

class module_wrapper(object):

    def __init__(self, modules):
        self.modules = modules
        if modules['Thema'] == 'True':
            import modules.themadesmonats as themadesmonats
            self.get_thema = themadesmonats.monthly_topic
        if modules['Distro'] == 'True':
            import modules.distrodesmonats as distrodesmonats
            self.get_distro = distrodesmonats.get_distro
        if modules['Github'] == 'True':
            import modules.github as github
            self.get_github = github.get_github
        if modules['Mumble'] == 'True':
            import modules.mumble as mumble
            self.get_mumble = mumble.get_mumble
        if modules['9gag'] == 'True':
            import modules.nine_gag as nine_gag
            self.get_nine_gag = nine_gag.get_meme
        if modules['Forum'] == 'True':
            import modules.forum as forum
            self.get_forum = forum.get_forum
        if modules['Facebook'] == 'True':
            import modules.fb as fb
            self.get_fb = fb.get_fb
        if modules['calc'] == 'True':
            import modules.calc as calc
            self.calc = calc.calc
        if modules['FAQ'] == 'True':
            import modules.faq as faq
            self.get_faq = faq.get_faq

    def get_response(self, cmd):
        cmd = re.sub('@.*', '', cmd)
        if cmd.startswith('/hilfe'):
            return self.get_help()
        elif cmd.startswith('/calc') and self.modules['calc'] == 'True':
            return self.calc(self.rm_command(cmd))
        elif cmd.startswith('/9gag') and self.modules['9gag'] == 'True':
            return self.get_nine_gag()
        elif cmd == '/lsw' and self.modules['Forum'] == 'True':
            return self.get_forum()
        elif cmd.startswith('/lsw'):
            cmd = re.sub('/lsw ', '', cmd)
            if cmd.startswith('Thema') and self.modules['Thema'] == 'True':
                return self.get_thema()
            elif cmd.startswith('Distro') and self.modules['Distro'] == 'True':
                return self.get_distro()
            elif cmd.startswith('FAQ') and self.modules['FAQ'] == 'True':
                return self.get_faq()
            elif cmd.startswith('Facebook') and self.modules['Facebook'] == 'True':
                return self.get_fb()
            elif cmd.startswith('Mumble') and self.modules['Mumble'] == 'True':
                return self.get_mumble()
            elif cmd.startswith('Github') and self.modules['Github'] == 'True':
                return self.get_github()
            elif cmd.startswith('Version') and self.modules['Version'] == 'True':
                return 'LsW-Plugins' \
                        + '\n\n/lsw: Bekomme den Link zu unserer Homepage.' \
                        + '\n/lsw Thema: Finde heraus, was das aktuelle Thema des Monats ist.' \
                        + '\n/lsw Distro: Finde heraus, welches die aktuelle Distro des Monats ist.' \
                        + '\n/lsw Mumble: Bekomme Infos über unsereren Mumble Server.' \
                        + '\n/lsw FAQ: Siehe unsere Antworten auf beliebte Fragen.' \
                        + '\n/lsw Facebook: Bekomme die Links zu unserer Facebook Gruppe und Seite.' \
                        + '\n/lsw Version: Bekomme Infos über das Plugin selbst.'
            elif not cmd.startswith(''):
                a = 1
        elif cmd.startswith('/'):
            return 'Ungültiger Befehl! ' + self.get_help()

    def get_help(self):
        help = 'Diese Befehle verstehe ich ;)\n'
        for i in self.modules:
            if self.modules[i] == 'True':
                if i == 'Facebook':
                    help += '\n/lsw Facebook: Bekomme die Links zu unserer Facebook Gruppe und Seite.'
                elif i == 'Thema':
                    help += '\n/lsw Thema: Finde heraus, was das aktuelle Thema des Monats ist.'
                elif i == 'Distro':
                    help += '\n/lsw Distro: Finde heraus, welches die aktuelle Distro des Monats ist.'
                elif i == 'Mumble':
                    help += '\n/lsw Mumble: Bekomme Infos über unsereren Mumble Server.'
                elif i == '9gag':
                    help += '\n/9gag - sendet ein zufälliges 9gag Meme'
                elif i == 'Forum':
                    help += '\n/lsw: Bekomme den Link zu unserer Homepage.'
                elif i == 'calc':
                    help += '\n/calc [Term] - Rechnet den Term aus(kein Punkt-vor-Strich/keine Klammern)'
                elif i == 'FAQ':
                    help += '\n/lsw FAQ: Siehe unsere Antworten auf beliebte Fragen.'
                elif i == 'Version':
                    help += '\n/lsw Version: Bekomme Infos über das Plugin selbst.'
        return help

    def rm_command(self, inp):
        exp = re.sub('\/[a-zA-Z]*\s', '', inp)
        return exp

