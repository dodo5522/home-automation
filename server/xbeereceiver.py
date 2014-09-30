#!/usr/bin/env python3

"""
 Class implementation to receive data of sensors via XBee.
 Editor     : Takashi Ando
 Version    : 1.0
"""

import datetime
import logging
import struct
import serial
from xbee import ZigBee

class SensorData(object):
    '''
    Class to store the data got from sensor.
    '''
    def __init__(self, sensor_id=None, value=0.0):
        if isinstance(sensor_id, str) is False:
            raise ValueError('sensor_id should be string.')
        self._sensor_id = sensor_id

        if isinstance(value, float) is False:
            raise ValueError('value should be float.')
        self._value = value

    def __str__(self):
        return self._sensor_id

    def __repr__(self):
        return self._sensor_id

    def get_value(self):
        '''
        Get the value.
        '''
        return self._value

    def set_value(self, value):
        '''
        Set the value.
        '''
        if isinstance(value, float) is False:
            raise ValueError('value should be float.')
        self._value = value

class XBeeNode(object):
    '''
    Class to store the information of XBee node.
    '''
    def __init__(self, node_name=None, source_addr_long=0, source_addr=0, sensor_ids=()):
        self._node_name = node_name
        self._source_addr_long = source_addr_long
        self._source_addr = source_addr

        self._sensor_data = []
        for sensor_id in sensor_ids:
            sensor_data = SensorData(sensor_id=sensor_id)
            self._sensor_data.append(sensor_data)

    def __str__(self):
        return self._node_name

    def __repr__(self):
        return self._node_name

    def set_source_addr_long(self, source_addr_long):
        '''
        '''
        self._source_addr_long = source_addr_long

    def set_source_addr(self, source_addr):
        '''
        '''
        self._source_addr = source_addr

class XBeeReceiver(object):
    '''
    Class with functions to communicate with XBee ZB.
    '''

    def __init__(self, port='/dev/ttyAMA0', baurate=9600, \
            sensors=5, debug_level=logging.WARN):
        '''
        port and baurate should be set to same values with XBee sensor module.
        And sensors should be set to the number of sensor mounted on it.
        '''
        log_format = '%(asctime)-15s %(module)-8s %(message)s'
        logging.basicConfig(format=log_format)

        self._logger = logging.getLogger('XBeeReceiver')
        self._logger.setLevel(debug_level)

        self._port = port
        self._baurate = baurate
        self._sensors = sensors
        ser = serial.Serial(self._port, self._baurate)
        self._xbee = ZigBee(ser, escaped=True)
        self._sensordata = SensorData(sensors=self._sensors)

    def wait_for_api_frame(self):
        '''
        Wait for API frame and store the parsed data got from XBee ZB.
        The parsed data is dictionary format.
        The parsed data can be got with get_parsed_data() method.
        '''

        data = self._xbee.wait_read_frame()

        src_addr_raw = [byte for byte in struct.unpack('BBBBBBBB', data['source_addr_long'])]
        self._parsed_data['source_addr_long'] = 0
        for i in range(0, 8):
            self._logger.info('SRC[%d]: %s'.format(i, hex(src_addr_raw[i])))
            self._parsed_data['source_addr_long'] |= src_addr_raw[i] << 8 * (7 - i)

        net_addr_raw = [byte for byte in struct.unpack('BB', data['source_addr'])]
        self._parsed_data['source_addr'] = 0
        for i in range(0, 2):
            self._logger.info('NET[%d]: %s'.format(i, hex(net_addr_raw[i])))
            self._parsed_data['source_addr'] |= net_addr_raw[i] << 8 * (1 - i)

        self._logger.info('ID: %s'.format(data['id']))
        self._parsed_data['id'] = data['id']

        #self._logger.info('OPT: %s'.format(data['options']))
        #self._parsed_data['options'] = data['options']

        rf_data_format = ['4sl' for i in range(0, self._sensors)]
        rf_data_format = ''.join(rf_data_format)
        rf_data = struct.unpack(rf_data_format, data['rf_data'])

        for rf_word_num in range(0, self._sensors):
            rf_data_4s = rf_data[rf_word_num*2+0]
            sensor_type = rf_data_4s.decode('ascii')

            rf_data_l = rf_data[rf_word_num*2+1]
            sensor_value = rf_data_l / 10.0

            self._parsed_data[sensor_type] = sensor_value
            self._logger.info('TYPE,VAL: %s,%f'.format(sensor_type, sensor_value))

    def get_parsed_data(self):
        '''
        Get the already parsed data.
        '''
        return self._parsed_data

