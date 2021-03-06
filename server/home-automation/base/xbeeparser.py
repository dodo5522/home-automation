#!/usr/bin/env python3

"""
 Class implementation to receive data of sensors via XBee.
 Editor     : Takashi Ando
 Version    : 1.0
"""

import logging
import struct

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
            self._logger.debug('src_addr[{0}]: {1}'.format(i, hex(src_addr_raw[i])))
            src_addr |= src_addr_raw[i] << 8 * (7 - i)

        return src_addr

    def get_source_addr(self, api_frame):
        '''
        Parse and return 'source_addr' (network address) value got from XBee node.
        '''
        net_addr_raw = [byte for byte in struct.unpack('BB', api_frame['source_addr'])]

        net_addr = 0
        for i in range(0, 2):
            self._logger.debug('net_addr[{0}]: {1}'.format(i, hex(net_addr_raw[i])))
            net_addr |= net_addr_raw[i] << 8 * (1 - i)

        return net_addr

    def get_id(self, api_frame):
        '''
        Parse and return 'id' value got from XBee node.
        '''
        self._logger.debug('id: {0}'.format(api_frame['id']))
        return api_frame['id']

    def get_options(self, api_frame):
        '''
        Parse and return 'options' value got from XBee node.
        '''
        self._logger.debug('opt: {0}'.format(api_frame['options']))
        return api_frame['options']

    def get_rf_data(self, api_frame):
        '''
        Parse and return 'rf_data' value got from XBee node.
        '''
        self._logger.debug('rf_data: {0}'.format(api_frame['rf_data']))
        return api_frame['rf_data']

class XBeeApiRfDataParser(XBeeApiFrameBaseParser):
    '''
    This class translate the API frame to sensor data.
    '''
    def __init__(self, sensors=0, log_level=logging.INFO):
        '''
        This parser should be initialized with the number of mounted sensors.
        '''
        self._sensors = sensors
        XBeeApiFrameBaseParser.__init__(self, log_level=log_level)

    def get_senser_data(self, api_frame):
        '''
        Parse and return the information from sensors mounted on XBee module.
        '''
        #FIXME: arduino for gardening should be updated at same time.
        #rf_data_format = ['4sll' for i in range(0, self._sensors)]
        rf_data_format = ['4sl' for i in range(0, self._sensors)]
        rf_data_format = ''.join(rf_data_format)
        rf_data = struct.unpack(rf_data_format, self.get_rf_data(api_frame))

        sensor_info = {}
        for rf_word_num in range(0, self._sensors):
            #FIXME: arduino for gardening should be updated at same time.
            #rf_data_4s = rf_data[rf_word_num * 3 + 0]
            rf_data_4s = rf_data[rf_word_num * 2 + 0]
            sensor_type = rf_data_4s.decode('ascii')

            #FIXME: arduino for gardening should be updated at same time.
            #rf_data_multiple = (float)(rf_data[rf_word_num * 3 + 1])
            #rf_data_value = rf_data[rf_word_num * 3 + 2]
            #sensor_value = rf_data_value / rf_data_multiple
            rf_data_value = rf_data[rf_word_num * 2 + 1]
            sensor_value = rf_data_value / 10.0

            sensor_info[sensor_type] = sensor_value
            self._logger.debug('type,value: {0},{1}'.format(sensor_type, sensor_value))

        return sensor_info

