#!/bin/sh

git clone https://github.com/iceman101184/ajaxcrud.git

cp -R ./ajaxcrud /var/www
cp -R ./css /var/www
cp -R ./images /var/www
cp index.php /var/www
cp ./ajaxcrud/javascript_functions.js /var/www
cp ./ajaxcrud/validation.js /var/www
