#!/bin/sh

sudo service nginx start
sudo service php$PHP_VERSION-fpm start
valet start