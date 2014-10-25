# Home automation

This repository is for my home automation by using Raspberry Pi and Arduino.  
The automated gardening is working now.  
Another function does not work yet.  

# System design

* Gardening monitoring
    * Written on [Qiita site](http://qiita.com/dodo5522/items/63d1efee3f70b3d5f2f6) in Japanese.
* Solar power monitoring
    * Under implementing.

# Directory structure

* documents
    * Overview, Schematics, etc.
* nodes
    * C/C++ source code working on Arduino.
    * All node will have Arduino and XBee.
* server [![Build Status](https://travis-ci.org/dodo5522/home-automation.svg?branch=master)](https://travis-ci.org/dodo5522/home-automation)
    * Python source code working on Raspberry Pi.
    * Raspberry Pi will work as server to gather the all information sent by all node.

# How to use

1. Locate 'setting.conf' with below values.

        $ cat /etc/home-automation/setting.conf
        [rpiuartreceiver]
        port = /dev/ttyAMA0
        baurate = 9600
        [vegetablesplantermonitor]
        address = 0x0013a20040b44f84
        xively_api_key = xxx
        xively_feed = yyy

2. Run the blew commands.

        $ git clone https://github.com/dodo5522/home-automation
        $ python3 ./home-automation/server/python/server.py

# Sequence flow

* server
    * Initialization and termination  
    ![initialize and terminate sequence flow](https://github.com/dodo5522/home-automation/blob/master/documents/uml/sequence_init_term.png)
    * Monitoring nodes  
    ![monitoring nodes](https://github.com/dodo5522/home-automation/blob/master/documents/uml/sequence_monitoring.png)
