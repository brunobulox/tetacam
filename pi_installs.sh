#!/bin/sh
apt-get update
apt-get upgrade
apt-get install -y  build-essentials sqlite3 libsqlite3 asterisk motion &&
 samba apache2 mysql-server php5 phpmyadmin super python-setuptools python-dev &&
 libmysqlclient-dev

# You will need to add 'Include /etc/phpmyadmin/apache.conf'
#  to /etc/apache2/apache2.conf at the end of the file


# To install watchdog you might have to  
#Edit /etc/init.d/skeleton and copy the LSB header (first ten lines or so) 
#from there to /etc/init.d/mathkernel  the init setup fails for me unless.
apt-get install watchdog


easy_install MySQL-python gdata


