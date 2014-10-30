#!/usr/bin/env python3

"""
 Server side code work on raspberry pi for my home automation.
 Editor     : Takashi Ando
 Version    : 1.0
"""
import serial
import logging
from xbee import ZigBee
from home_automation.base import process
from home_automation.base import xbeeparser

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

        self._monitors = monitors
        for monitor in self._monitors:
            monitor.start()

        self._port = port
        self._baurate = baurate
        self._ser = serial.Serial(self._port, self._baurate)
        self._xbee = ZigBee(self._ser, escaped=True, callback=self._receive_frame)

    def _receive_frame(self, api_frame):
        '''
        _receive_frame: XBee API frame dictionary -> None

        Callback to receive API frame from XBee module.
        And if the API frame has monitoring address, pass the frame to the monitor instance.
        '''
        self._logger.debug(api_frame)

        #TODO: unefficient way to search...
        for monitor in self._monitors:
            addr = self.get_source_addr_long(api_frame)
            if addr == monitor.get_monitoring_address():
                monitor.post_data_to_service(api_frame)

    def _do_terminate(self):
        '''Wait and join all thread and process.
        '''
        # halt() must be called before closing the serial
        # port in order to ensure proper thread shutdown
        self._xbee.halt()
        self._ser.close()

        for monitor in self._monitors:
            monitor.post_terminate()
            monitor.join(30)

