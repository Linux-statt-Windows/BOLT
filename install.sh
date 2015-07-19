#!/bin/bash

cp -R ../BOLT /opt/
ln -s /opt/BOLT/src/bolt.py /usr/bin/bolt

cp /opt/BOLT/conf/bolt /etc/bolt
cp /opt/BOLT/bolt.service /etc/systemd/system/bolt.service
