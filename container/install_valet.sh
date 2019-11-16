#!/bin/sh

echo 'Installing valet composer dep'
composer global require cpriego/valet-linux

echo 'Running valet install'
valet install
mkdir $DOMAINS
cd $DOMAINS
valet domain $DOMAIN_SUFFIX
valet park