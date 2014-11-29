#!/bin/bash

cd server

python3 ./setup.py build
sudo python3 ./setup.py install

[ -d /etc/home_automation ]              || sudo mkdir /etc/home_automation
[ -e /etc/home_automation/setting.conf ] || sudo cp ./etc/home-automation/setting.conf /etc/home_automation/
[ -e /etc/init.d/home-automation ]       || sudo cp ./etc/init.d/home-automation /etc/init.d/

