#!/usr/bin/env python3

"""
 Server side code work on raspberry pi for my home automation.
 Editor     : Takashi Ando
 Version    : 1.0
"""
import logging
from base_modules import xbeereceiver
from base_modules import config

class RPiUartReceiver(\
        xbeereceiver.ReceiverProcess,\
        config.Configuration):
    '''
    Process to receive data from XBee.
    There should be only one instance against one XBee coordinator.
    '''
    def __init__(self, monitors, log_level=logging.INFO):
        self._logger = logging.getLogger(type(self).__name__)
        self._logger.setLevel(log_level)

        config.Configuration.__init__(self, log_level=log_level)

        self._port = self.read_config('port')
        self._baurate = self.read_config('baurate', int)

        if self._port is None:
            raise ValueError('Serial port is not defined on conf file.')
        if self._baurate is None:
            raise ValueError('Serial baurate is not defined on conf file.')

        xbeereceiver.ReceiverProcess.__init__(monitors, self._port, self._baurate, log_level=log_level)

if __name__ == '__main__':
    config_test = []
    config_test.append('[rpiuartreceiver]\n')
    config_test.append('port = /dev/tty0\n')
    config_test.append('baurate = 9600\n')

    fp = open('setting.conf', 'w')
    for line in config_test:
        fp.write(line)
    fp.close()

    #FIXME: dummy monitor instance is needed!
    test_receiver = RPiUartReceiver(RPiUartReceiver, log_level=logging.DEBUG)

    print(test_receiver._port)
    print(test_receiver._baurate)

