#!/usr/bin/env python3

"""
 Server side code for my gardening.
 Editor     : Takashi Ando
 Version    : 1.0
"""

import sys
import datetime
import struct
import time
import multiprocessing
import xively
from requests.exceptions import HTTPError
from xbeereceiver import XBeeApiFrameParser

class GardeningMonitor(multiprocessing.Process, XBeeApiFrameParser):
    '''
    This class monitors gardening status with XBee.
    And put the information to Xively.
    '''

    _XIVELY_FEED_ID = 1779591762
    _XIVELY_ID_TABLE = \
    {
        'LUX0':'Luminosity',
        'HUM0':'Humidity',
        'MOI0':'MoistureOfSmallPlant',
        'MOI1':'MoistureOfLargePlant',
        'TMP0':'Temperature',
    }

    def __init__(self, target=None, name=None, args=(), kwargs={}):
        multiprocessing.Process.__init__(self, \
                target=target, name=name, args=args, kwargs=kwargs, daemon=None)

        if len(sys.argv) > 1:
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
            try:
                if xbee is None:
                    ser.read()
                else:
                    datastreams = []
                    parse()
                    now = datetime.datetime.utcnow()
                    self._logger.info(now)
                    datastreams.append(xively.Datastream(id=_XIVELY_ID_TABLE[sensor_type], current_value=sensor_value, at=now))
                    feed.datastreams = datastreams
                    feed.update()
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


