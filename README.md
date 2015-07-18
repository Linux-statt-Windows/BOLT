# BOLT
(B)OLT (O)perator for (L)sW (T)elegram Groups. Ein Bot für die LsW-Telegram Gruppen.


Features
--------

- Easy to use Python bot for the official Telegram API
- Fully modulised
- Easy to configure
- Send photos or text messages
- Restricted to one group
- Run in background


Install
-------

- Copy conf/bolt to /etc/bolt
- Set up your config(`/etc/bolt`) correctly!
- Run bolt with sudo(write to save-file in /var/lib/bolt/)

*Requierments: `python-requests(python 3)`*
*Disclaimer: the modules have to stay in their folder with their relative paths to BOLT*


Input Parameters
----------------

```
usage: bolt.py [-h] [--token TOKEN] [--interval INTERVAL]
               [--group-id GROUP_ID]

optional arguments:
  -h, --help           show this help message and exit
  --token TOKEN        token of your bot
  --interval INTERVAL  interval between two updates
  --group-id GROUP_ID  ID of your telegram-group
  -b, --background     starts bot in background
```


Modules
-------

- Forum
    - Facebook
    - Thema des Monats
    - Distri des Monats
    - Github
    - Mumble
    - FAQ
- 9gag
- Calc
- Meme Generator
- Hackernews
- Google (works, but is very very slow)
- DuckDuckGo (not working at the moment!)
- QR-Code Generator
- Wetter
- XKCD
- OMDB
- Bitcoin


License
-------
Licensed under GNU General Public License.
See [LICENSE](./LICENSE) for details.
