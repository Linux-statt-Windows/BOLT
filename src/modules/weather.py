#!/bin/env python3

import urllib.request
import json

URL = 'http://api.openweathermap.org/data/2.5/weather?'

def callback():
    return '/wetter', get_weather


def get_weather(inp):
    req = ''
    for i in inp:
        req += i
    req = {
            "q":req,
            "units":"metric"
            }
    req = urllib.parse.urlencode(req)
    rqst = urllib.request.urlopen(URL + req)
    data = json.loads(rqst.read().decode('utf-8'))
    if data['weather'][0]['main'] == 'Clear':
        icon = ' ☀'
    elif data['weather'][0]['main'] == 'Clouds':
        icon = ' ☁☁'
    elif data['weather'][0]['main'] == 'Rain':
        icon = ' ☔'
    elif data['weather'][0]['main'] == 'Thunderstorm':
        icon = ' ☔☔☔☔'

    return 'Wetter in: ' + data['name'] \
            + '\n\nTemperatur: ' + str(data['main']['temp']) + '°C' \
            + '\nMin. Temperatur: ' + str(data['main']['temp_min']) + '°C' \
            + '\nMax. Temperatur: ' + str(data['main']['temp_max']) + '°C' \
            + '\nWetter: ' + icon \
            + '\nWindgeschwindigkeit: ' + str(data['wind']['speed'])


def get_help():
    return '\n/wetter [Stadt]: Gibt das Wetter der Stadt aus'


if __name__ == '__main__':
    print(get_weather(['Oberhausen']))
