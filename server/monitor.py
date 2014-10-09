#!/usr/bin/env python3

"""
 Server side code of base class for monitoring.
 Editor     : Takashi Ando
 Version    : 1.0
"""

import datetime
import logging
import xively
import xbeeparser

class BaseMonitor(xbeeparser.XBeeApiRfDataParser):
    '''
    base class to monitor one xbee module node.
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
        XBee source address, xively api key, and feed id are needed.
        '''
        self._logger = logging.getLogger(name=type(self).__name__)
        self._logger.setLevel(log_level)

        self._monitoring_address = monitoring_address

        api = xively.XivelyAPIClient(xively_api_key)
        self._xively_feed = api.feeds.get(xively_feed_id)

    def parse(self, api_frame):
        '''
        Parse api frame.
        '''
        if self.get_source_addr_long(api_frame) != self._monitoring_address:
            return None
        else:
            return self.get_senser_data(api_frame)

    def post_data(self, sensor_type, sensor_value):
        '''
        Post sensor data to Xively service.
        '''
        now = datetime.datetime.utcnow()
        self._logger.info(now)

        #FIXME: data structure is not matched to the one of xbee node.
        datastreams = []
        for sensor_info in BaseMonitor._XIVELY_ID_TABLE:
            datastreams.append(xively.Datastream(id=sensor_info[sensor_type], current_value=sensor_value, at=now))
        self._xively_feed.datastreams = datastreams
        self._xively_feed.update()

