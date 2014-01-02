#!/bin/sh

case $1 in
start)
super motion
;;
stop)
super pkill -9 motion
;;
esac
