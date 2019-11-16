#!/bin/sh

$apti npm nodejs libpng-dev
npm config set registry https://registry.npmjs.org/
npm install npm@latest -g