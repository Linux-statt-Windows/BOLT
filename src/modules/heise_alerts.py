from html.parser import HTMLParser
#from html.parser import HTMLParseError
import requests
import re

class HeiseAlertParser ( HTMLParser ):
    __alertSectionClass = 'liste_alerts'
    __insideAlertSection = False
    __sectionTag = 'section'
    __linkTag = 'a'
    __alertList = list()

    def __init_ ( self ):
        HTMLParser.__init__ ( self )

    def handle_starttag ( self, tag, attributes ):
        attr = self.__attributesToDict ( attributes )
        if tag == self.__sectionTag and attr.get('class', ' ') == self.__alertSectionClass:
            self.__insideAlertSection = True
        elif tag == self.__linkTag and self.__insideAlertSection:
            href = attr['href']
            href = 'http://www.heise.de' + href
            title = attr['title']
            self.__alertList.append ( (href, title) )

    def __attributesToDict ( self, attr ):
        dict_ = {}
        for t in attr:
            key_ = t[0]
            val_ = t[1]
            dict_[key_] = val_

        return dict_

    def handle_endtag ( self, tag ):
        if tag == self.__sectionTag and self.__insideAlertSection:
            self.__insideAlertSection = False

    def getAlert ( self ):
        return self.__alertList

    def feed ( self, data ):
        self.__insideAlertSection = False
        self.__alertList.clear()
        super().feed ( data )
        return self.__alertList

def callback():
    #print ( "alerts callback")
    return '/heisealerts', get_alerts

def get_alerts(inp):
    #print ( "getting heise alerts.." )
    parser = HeiseAlertParser()
    page = requests.get ( 'http://www.heise.de/security/' ).text
    alerts = parser.feed ( page )
    ret = ""
    for alert in alerts:
        ret += alert[1] + "\n  " + alert[0] + "\n"
    return ret

def get_help():
    return "\n/heisealerts: Gibt die aktuellen Alerts von Heise-Security aus"

def main():
    print ( get_alerts("") )

if __name__ == '__main__':
    main()
