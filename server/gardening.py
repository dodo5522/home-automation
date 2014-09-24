#!/usr/bin/env python3

"""
 Example code for server side on raspberry pi for my gardening.
 Editor     : Takashi Ando
 Version    : 1.0
"""
from xbee import ZigBee
from requests.exceptions import HTTPError
import sys
import datetime
import struct
import time
import serial
import xively

_XBEE_PORT = '/dev/ttyAMA0'
_XBEE_BAUDRATE = 9600

_XIVELY_API_KEY = 'ov5DHZ4sIWyS4M5wiNthJjKmkwtZmRAR3lKCzsBOdjKN0Tgm'
_XIVELY_FEED_ID = 1779591762
_XIVELY_ID_TABLE = \
{
        'LUX0':'Luminosity',
        'HUM0':'Humidity',
        'MOI0':'MoistureOfSmallPlant',
        'MOI1':'MoistureOfLargePlant',
        'TMP0':'Temperature',
}

def message_received(feed, data, now):
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

if __name__ == '__main__':
    ser = serial.Serial(_XBEE_PORT, _XBEE_BAUDRATE)

    api = xively.XivelyAPIClient(_XIVELY_API_KEY)
    feed = api.feeds.get(_XIVELY_FEED_ID)
    
    kargs = {}
    kargs['escaped'] = True
    #kargs['callback'] = message_received
    
    # Create API object, which spawns a new thread
    if len(sys.argv) > 1:
        xbee = None
    else:
        xbee = ZigBee(ser, **kargs)
    
    # Do other stuff in the main thread
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
