#!/bin/sh
apt-get update
apt-get upgrade
apt-get install -y  build-essentials sqlite3 libsqlite3 asterisk motion &&
 samba apache2 mysql-server php5 phpmyadmin super python-setuptools python-dev &&
 libmysqlclient-dev

easy_install MySQL-python gdata

 
# You will need to add 'Include /etc/phpmyadmin/apache.conf'
#  to /etc/apache2/apache2.conf at the end of the file
