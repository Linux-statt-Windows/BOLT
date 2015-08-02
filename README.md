# BOLT
(B)OLT (O)perator for (L)inux statt Windows (T)elegram groups. A bot for "Linux statt Windows" telegram groups.


Features
--------

- Easy to use Python bot for the official Telegram API
- Fully modulised
- Easy to configure
- Send photos or text messages
- Restricted to one group
- Run in background
- Call modules in intervals
- Run as systemd service
- Run multiple bots in different threads with different config-files
- Sends a notification to a specific group-/chat-id, if banned username rejoins the group


Install
-------

- Clone this git to `/opt/`
- Run the `install.sh`
- Run bolt with sudo(write to save-file in /var/lib/bolt/) or as a systemd service

*Requierments: `python-requests(python 3)`*

*Disclaimer: the modules have to stay in their folder with their relative paths to BOLT*


Input Parameters
----------------

```
usage: bolt.py [-h] [--token TOKEN] [--interval INTERVAL]
               [--group-id GROUP_ID]

optional arguments:
  -h, --help           show this help message and exit
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
- Google (works, but it is very very slow)
- QR-Code Generator
- Wetter
- XKCD
- OMDB
- Bitcoin
- Reminder(work in progress)
- daujones


License
-------

Licensed under GNU General Public License.
See [LICENSE](./LICENSE) for details.
