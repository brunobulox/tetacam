#!/bin/sh

case $1 in
start)
sudo service  motion start
;;
stop)
sudo service motion stop
;;
esac
