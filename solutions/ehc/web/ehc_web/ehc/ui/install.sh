#!/usr/bin/env bash
# Install
## NodeJS 5.x
sudo apt-get purge -y node npm
sudo apt-get install curl build-essential
curl -sL https://deb.nodesource.com/setup_5.x | sudo -E bash -
sudo apt-get install -y nodejs

## NPM global cli
sudo npm isntall -g bower
sudo npm install -g gulp
sudo npm install -g karma-cli