#!/bin/sh
echo "create database tetacam" | mysql -u root -p
cat tetacam.sql | mysql -u root -p tetacam
