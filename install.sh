#!/bin/bash

cp -R ../BOLT /opt/
ln -s /opt/BOLT/src/bolt.py /usr/bin/bolt

mkdir /etc/channel.d/
cp /opt/BOLT/conf/bolt /etc/channel.d/bolt
cp /opt/BOLT/bolt.service /etc/systemd/system/bolt.service
