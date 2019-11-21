#!/bin/sh

sudo chown -R $DEV_USER:$DEV_USER ${DEV_HOME}/.valet
sudo service nginx start
sudo service php$PHP_VERSION-fpm start
valet start