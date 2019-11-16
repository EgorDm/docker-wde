#!/bin/sh

PHP_CLI_INI=$(php -i | grep /.+/php.ini -oE)
PHP_FPM_INI=$(echo "$PHP_CLI_INI" | sed  s/cli/fpm/)

php_config() {
  sed -i "s/^$1.*=.*/$1 = $2/" $PHP_CLI_INI
  sed -i "s/^$1.*=.*/$1 = $2/" $PHP_FPM_INI
}

php_config max_execution_time 0
php_config display_errors On
php_config display_startup_errors On
php_config track_errors On
php_config max_file_uploads 200
php_config upload_max_filesize 20M
php_config max_input_vars 10000

sed s/www-data/magnetron/ -i /etc/php/$PHP_VERSION/fpm/pool.d/www.conf

{
  echo "xdebug.default_enable=1"
  echo "xdebug.remote_autostart=0"
  echo "xdebug.remote_enable=1"
  echo "xdebug.remote_connect_back=1"
  echo "xdebug.max_nesting_level=500"
  echo "xdebug.idekey=PHPSTORM"
} >> /etc/php/$PHP_VERSION/mods-available/xdebug.ini

{
  echo "opcache.revalidate_freq=0"
  echo "opcache.validate_timestamps=1"
  echo "opcache.max_accelerated_files=10000"
  echo "opcache.memory_consumption=192"
  echo "opcache.max_wasted_percentage=10"
  echo "opcache.interned_strings_buffer=16"
  echo "opcache.fast_shutdown=1"
  echo "opcache.dups_fix=1"
} >> /etc/php/$PHP_VERSION/mods-available/opcache.ini