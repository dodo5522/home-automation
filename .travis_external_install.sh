#!/bin/bash
pip install pyserial
git clone https://github.com/xively/xively-python.git
cd xively-python
python ./setup.py build
python ./setup.py install
cd -
hg clone https://code.google.com/p/python-xbee
cd python-xbee
python ./setup.py build
python ./setup.py install
cd -
