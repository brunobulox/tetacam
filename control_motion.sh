#!/bin/sh

case $1 in
start)
sudo service  motion start
;;
stop)
sudo  pkill -9 motion
;;
esac
