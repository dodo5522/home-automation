#!/usr/bin/env python3

"""
 Server side code work on raspberry pi for my home automation.
 Editor     : Takashi Ando
 Version    : 1.0
"""
import threading
import serial
import logging
from xbee import ZigBee
from base_modules import process
from base_modules import xbeeparser

class ReceiverProcess(\
        process.BaseProcess,
        xbeeparser.XBeeApiFrameBaseParser):
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

        process.BaseProcess.__init__(self, log_level=log_level)
        xbeeparser.XBeeApiFrameBaseParser.__init__(self, log_level=log_level)

        self._port = port
        self._baurate = baurate
        self._ser = serial.Serial(self._port, self._baurate)
        self._xbee = ZigBee(self._ser, escaped=True)

        self._monitors = monitors
        for monitor in self._monitors:
            monitor.start()

        self._thread_receive = threading.Thread(target=self._receive_frame)
        self._thread_receive.start()

    def _receive_frame(self):
        '''Wait for API frame from XBee module.
           And return the node information (source address etc.) and another data.
        '''
        while True:
            api_frame = self._xbee.wait_read_frame()
            self._logger.debug(api_frame)

            #TODO: unefficient way to search...
            for monitor in self._monitors:
                addr = self.get_source_addr_long(api_frame)
                if addr == monitor.get_monitoring_address():
                    monitor.post_data(api_frame)

        self._logger.debug('thread to receive is done.')

    def _do_terminate(self):
        '''Wait and join all thread and process.
        '''
        self._xbee.halt()
        self._thread_receive.join(30)

        for monitor in self._monitors:
            monitor.post_terminate()
            monitor.join(30)

        # halt() must be called before closing the serial
        # port in order to ensure proper thread shutdown
        if self._xbee is not None:
            self._xbee.halt()
        self._ser.close()

