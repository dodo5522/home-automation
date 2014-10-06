# Home automation

This repository is for my home automation by using Raspberry Pi and Arduino.  
The automated gardening is working now.  
Another function does not work yet.  

# System design

* Gardening
    * Written on [Qiita site](http://qiita.com/dodo5522/items/63d1efee3f70b3d5f2f6) in Japanese.

# Directory structure

* documents
    * Overview, Schematics, etc.
* nodes
    * C/C++ source code working on Arduino.
    * All node will have Arduino and XBee.
* server
    * Python source code working on Raspberry Pi.
    * Raspberry Pi will work as server to gather the all information sent by all node.

# Sequence flow

* Initialization and termination
    ![initialize and terminate sequence flow](https://github.com/dodo5522/home-automation/blob/master/documents/uml/sequence_init_term.png)
