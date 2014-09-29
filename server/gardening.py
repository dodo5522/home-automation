#!/usr/bin/env python3

"""
 Example code for server side on raspberry pi for my gardening.
 Editor     : Takashi Ando
 Version    : 1.0
"""
import sys
import datetime
import struct
import time
import multiprocessing
import serial
import xively
from xbee import ZigBee
from requests.exceptions import HTTPError

class GardeningMonitor(multiprocessing.Process):
    _XBEE_PORT = '/dev/ttyAMA0'
    _XBEE_BAUDRATE = 9600
    
    _XIVELY_FEED_ID = 1779591762
    _XIVELY_ID_TABLE = \
    {
            'LUX0':'Luminosity',
            'HUM0':'Humidity',
            'MOI0':'MoistureOfSmallPlant',
            'MOI1':'MoistureOfLargePlant',
            'TMP0':'Temperature',
    }

    def __init__(self, group=None, target=None, name=None, args=(), kwargs={}):
        multiprocessing.Process.__init__(self, group=group, target=target,\
                name=name, args=args, kwargs=kwargs, daemon=None)

        ser = serial.Serial(self._XBEE_PORT, self._XBEE_BAUDRATE)

        if len(sys.argv) > 1:
            if 'debug' in sys.argv:
                xbee = None
            else:
                xbee = xbee.ZigBee(ser, escaped=True)
                api = xively.XivelyAPIClient(sys.argv[1])
                feed = api.feeds.get(_XIVELY_FEED_ID)
        else:
            raise SystemError('Xively API key is required.')

    def run(self):
        '''
        Method to be run in sub-process; can be overridden in sub-class
        '''
        if self._target:
            self._target(*self._args, **self._kwargs)
        else:
            while True:
                try:
                    if xbee is None:
                        ser.read()
                    else:
                        data = xbee.wait_read_frame()
                        now = datetime.datetime.utcnow()
                        message_received(feed, data, now)
                except HTTPError:
                    print('HTTPError occurs.')
                    time.sleep(600)
                    continue
                except KeyboardInterrupt:
                    break

            # halt() must be called before closing the serial
            # port in order to ensure proper thread shutdown
            if xbee is not None:
                xbee.halt()
            ser.close()

    def _parse_xbee_data(data, now):
        print(now)
    
        source_addr_long_raw = [byte for byte in struct.unpack('BBBBBBBB', data['source_addr_long'])]
    
        source_addr_long_high = 0
        for i in range(0,4):
            source_addr_long_high |= source_addr_long_raw[i] << 8 * (3 - i)
        print(hex(source_addr_long_high))
    
        source_addr_long_low = 0
        for i in range(4,8):
            source_addr_long_low |= source_addr_long_raw[i] << 8 * (7 - i)
        print(hex(source_addr_long_low))
        
        source_addr_raw = [byte for byte in struct.unpack('BB', data['source_addr'])]
    
        source_addr = 0
        for i in range(0,2):
            source_addr |= source_addr_raw[i] << 8 * (1 - i)
        print(hex(source_addr))
    
        #print(data['id'])
        #print(data['options'])
    
        rf_data = struct.unpack('4sl4sl4sl4sl4sl', data['rf_data'])
    
        datastreams = []
        for rf_word_num in range(0,5):
            sensor_type  = rf_data[rf_word_num*2+0].decode('ascii')
            sensor_value = rf_data[rf_word_num*2+1] / 10.0
            print(sensor_type, sensor_value)
    
            datastreams.append(xively.Datastream(id=_XIVELY_ID_TABLE[sensor_type], current_value=sensor_value, at=now))
    
        feed.datastreams = datastreams
        feed.update()

