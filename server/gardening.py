#!/usr/bin/env python3

"""
 Server side code for my gardening.
 Editor     : Takashi Ando
 Version    : 1.0
"""

import xively
import datetime
import logging
from base_modules import process
from base_modules import xbeeparser

class VegetablesPlanterMonitor(\
        process.BaseProcess,
        xbeeparser.XBeeApiRfDataParser):
    '''
    This class monitors gardening status with XBee.
    And put the information to Xively.
    '''

    _XIVELY_ID_TABLE = \
    {
        'LUX0':'Luminosity',
        'HUM0':'Humidity',
        'MOI0':'MoistureOfSmallPlant',
        'MOI1':'MoistureOfLargePlant',
        'TMP0':'Temperature',
    }

    def __init__(self, monitoring_address, xively_api_key, xively_feed_id, log_level=logging.INFO):
        '''
        Initialize process etc.
        '''
        process.BaseProcess.__init__(self, log_level=log_level)

        self._monitoring_address = monitoring_address

        api = xively.XivelyAPIClient(xively_api_key)
        self._xively_feed = api.feeds.get(xively_feed_id)

        self._message_table[1] = self._do_post_data

    def _do_terminate(self):
        '''Terminate procedure internally.
        '''
        pass

    def parse(self, api_frame):
        '''
        Parse api frame.
        '''
        if self.get_source_addr_long(api_frame) != self._monitoring_address:
            return None
        else:
            return self.get_senser_data(api_frame)

    def post_data(self, sensor_type, sensor_value):
        #FIXME: not implemented yet.
        raise NotImplementedError

    def _do_post_data(self, sensor_type, sensor_value):
        '''
        Post sensor data to Xively service.
        '''
        now = datetime.datetime.utcnow()
        self._logger.info(now)

        #FIXME: data structure is not matched to the one of xbee node.
        datastreams = []
        for sensor_info in VegetablesPlanterMonitor._XIVELY_ID_TABLE:
            datastreams.append(xively.Datastream(id=sensor_info[sensor_type], current_value=sensor_value, at=now))
        self._xively_feed.datastreams = datastreams
        self._xively_feed.update()

