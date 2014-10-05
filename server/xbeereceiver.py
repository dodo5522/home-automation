#!/usr/bin/env python3

"""
 Class implementation to receive data of sensors via XBee.
 Editor     : Takashi Ando
 Version    : 1.0
"""

import logging
import struct
import serial
from xbee import ZigBee

class XBeeApiFrameBaseParser(object):
    '''
    This class translate the API frame to node information.
    '''
    def __init__(self, log_level=logging.INFO):
        '''
        This parser should be initialized with the number of mounted sensors.
        '''
        self._logger = logging.getLogger(type(self).__name__)
        self._logger.setLevel(log_level)

    def get_source_addr_long(self, api_frame):
        '''
        Parse and return 'source_addr_long' value got from XBee node.
        '''
        src_addr_raw = [byte for byte in struct.unpack('BBBBBBBB', api_frame['source_addr_long'])]

        src_addr = 0
        for i in range(0, 8):
            self._logger.info('SRC[%d]: %s'.format(i, hex(src_addr_raw[i])))
            src_addr |= src_addr_raw[i] << 8 * (7 - i)

        return src_addr

    def get_source_addr(self, api_frame):
        '''
        Parse and return 'source_addr' (network address) value got from XBee node.
        '''
        net_addr_raw = [byte for byte in struct.unpack('BB', api_frame['source_addr'])]

        net_addr = 0
        for i in range(0, 2):
            self._logger.info('NET[%d]: %s'.format(i, hex(net_addr_raw[i])))
            net_addr |= net_addr_raw[i] << 8 * (1 - i)

        return net_addr

    def get_id(self, api_frame):
        '''
        Parse and return 'id' value got from XBee node.
        '''
        self._logger.info('ID: %s'.format(api_frame['id']))
        return api_frame['id']

    def get_options(self, api_frame):
        '''
        Parse and return 'options' value got from XBee node.
        '''
        self._logger.info('OPT: %s'.format(api_frame['options']))
        return api_frame['options']

class XBeeApiFrameParser(XBeeApiFrameBaseParser):
    '''
    This class translate the API frame to node information and sensor data.
    '''
    def __init__(self, sensors=0, log_level=logging.INFO):
        '''
        This parser should be initialized with the number of mounted sensors.
        '''
        self._sensors = sensors
        self._logger = logging.getLogger(type(self).__name__)
        self._logger.setLevel(log_level)

    def get_sensed_info(self, api_frame):
        '''
        Parse and return the information from sensors mounted on XBee module.
        '''
        rf_data_format = ['4sl' for i in range(0, self._sensors)]
        rf_data_format = ''.join(rf_data_format)
        rf_data = struct.unpack(rf_data_format, api_frame['rf_data'])

        sensor_info = {}
        for rf_word_num in range(0, self._sensors):
            rf_data_4s = rf_data[rf_word_num*2+0]
            sensor_type = rf_data_4s.decode('ascii')

            rf_data_l = rf_data[rf_word_num*2+1]
            sensor_value = rf_data_l / 10.0

            sensor_info[sensor_type] = sensor_value
            self._logger.info('TYPE,VAL: %s,%f'.format(sensor_type, sensor_value))

        return sensor_info

class XBeeReceiver(XBeeApiFrameBaseParser):
    '''
    Class with functions to communicate with XBee ZB.
    There should be only one instance against one XBee coordinator.
    '''

    def __init__(self, port='/dev/ttyAMA0', baurate=9600, log_level=logging.INFO):
        '''
        Initialize XBee instance with serial port and baurate.
        The baurate should be set to same value with XBee module.
        '''
        self._logger = logging.getLogger(type(self).__name__)
        self._logger.setLevel(log_level)

        self._port = port
        self._baurate = baurate
        ser = serial.Serial(self._port, self._baurate)
        self._xbee = ZigBee(ser, escaped=True)

    def wait_for_api_frame(self):
        '''
        Wait for API frame from XBee module.
        And return the node information (source address etc.) and another data.
        '''
        return self._xbee.wait_read_frame()

