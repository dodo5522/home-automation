#!/usr/bin/env python3

"""
 Server side code work on raspberry pi for my home automation.
 Editor     : Takashi Ando
 Version    : 1.0
"""
import multiprocessing
import serial
import logging
from xbee import ZigBee
from base_modules import XBeeApiFrameBaseParser

class ReceiverProcess(\
        multiprocessing.Process,\
        XBeeApiFrameBaseParser):
    '''
    Base class of process to receive data from XBee ZB.
    There should be only one instance against one XBee coordinator.
    '''
    def __init__(self, monitors, port='/dev/ttyAMA0', baurate=9600, log_level=logging.INFO):
        '''Initialize XBee instance with serial port and baurate.
           The baurate should be set to same value with XBee module.
        '''
        self._logger = logging.getLogger(type(self).__name__)
        self._logger.setLevel(log_level)

        self._port = port
        self._baurate = baurate
        self._ser = serial.Serial(self._port, self._baurate)
        self._xbee = ZigBee(self._ser, escaped=True)

        self._monitors = monitors

    def run(self):
        '''Wait for API frame from XBee module.
           And return the node information (source address etc.) and another data.
        '''
        for monitor in self._monitors:
            monitor.start()

        while True:
            try:
                api_frame = self._xbee.wait_read_frame()

                #FIXME: monitor can return or has address
                if self.get_source_addr_long(api_frame) in self._monitors:
                    monitor.post_data(api_frame)

            except Exception as err:
                print('{0} occurs.'.format(err))
                continue

    def terminate(self):
        '''Terminate this process and wait all monitor process joined.
        '''
        for monitor in self._monitors:
            monitor.terminate()
            monitor.join(30)

        # halt() must be called before closing the serial
        # port in order to ensure proper thread shutdown
        if self._xbee is not None:
            self._xbee.halt()
        self._ser.close()

