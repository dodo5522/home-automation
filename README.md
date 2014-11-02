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

1. Raspberry Pi as XBee cordinator
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
            $ cd ./home-automation/server
            $ python3 ./setup.py build
            $ sudo python3 ./setup.py install
            $ nohup python3 -m home_automation &

2. Arduino with XBee router
    1. Use Arduino IDE 1.5.8 or later.
    2. Add c++11 flag on Arduino toolchain setting files. You can find the file like below.

            $ find /Applications/Arduino.app -name platform.txt
            /Applications/Arduino.app/Contents/Resources/Java/hardware/arduino/avr/platform.txt
            /Applications/Arduino.app/Contents/Resources/Java/hardware/arduino/sam/platform.txt

    3. Add flag setting onto both of the above setting file.

            --- origin.txt	2014-11-03 01:01:18.000000000 +0900
            +++ modify.txt	2014-11-03 01:01:03.000000000 +0900
            @@ -17,7 +17,7 @@
             compiler.c.elf.flags=-Os -Wl,--gc-sections
             compiler.S.flags=-c -g -x assembler-with-cpp
             compiler.cpp.cmd=arm-none-eabi-g++
            -compiler.cpp.flags=-c -g -Os -w -ffunction-sections -fdata-sections -nostdlib -fno-threadsafe-statics --param max-inline-insns-single=500 -fno-rtti -fno-exceptions -Dprintf=iprintf
            +compiler.cpp.flags=-std=gnu++11 -c -g -Os -w -ffunction-sections -fdata-sections -nostdlib -fno-threadsafe-statics --param max-inline-insns-single=500 -fno-rtti -fno-exceptions -Dprintf=iprintf
             compiler.ar.cmd=arm-none-eabi-ar
             compiler.ar.flags=rcs
             compiler.objcopy.cmd=arm-none-eabi-objcopy

    4. Build and program Arduino with gardening or powerplant library.

# Sequence flow

* server
    * Initialization and termination  
    ![initialize and terminate sequence flow](https://github.com/dodo5522/home-automation/blob/master/documents/uml/sequence_init_term.png)
    * Monitoring nodes  
    ![monitoring nodes](https://github.com/dodo5522/home-automation/blob/master/documents/uml/sequence_monitoring.png)
