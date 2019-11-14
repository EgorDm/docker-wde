#!/bin/sh

PHP_CLI_INI=$(php -i | grep /.+/php.ini -oE)
PHP_FPM_INI=$(echo "$PHP_CLI_INI" | sed  s/cli/fpm/)

php_config() {
  sudo sed -i "s/^$1.*=.*/$1 = $2/" $PHP_CLI_INI
  sudo sed -i "s/^$1.*=.*/$1 = $2/" $PHP_FPM_INI
}

php_config max_execution_time 0
php_config display_errors On
php_config display_startup_errors On
php_config track_errors On
php_config upload_max_filesize 20M

sudo sed s/www-data/magnetron/ -i /etc/php/7.1/fpm/pool.d/www.conf


sudo bash -c 'printf "\nxdebug.remote_enable=1\nxdebug.remote_connect_back=1" >> /etc/php/7.1/mods-available/xdebug.ini'
