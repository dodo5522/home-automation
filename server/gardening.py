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
        xbeeparser.XBeeApiRfDataParser(self, sensors=len(VegetablesPlanterMonitor._XIVELY_ID_TABLE), log_level=log_level)

        self._monitoring_address = monitoring_address

        api = xively.XivelyAPIClient(xively_api_key)
        self._xively_feed = api.feeds.get(xively_feed_id)

        self._message_table[1] = self._do_post_data_to_service

    def get_monitoring_address(self):
        '''
        get_monitoring_address: None -> int

        Get XBee 64bit source address to monitor in this instance.
        '''
        return self._monitoring_address

    def post_data_to_service(self, api_frame):
        '''
        post_data_to_service: XBee API frame dictionary -> None

        Post monitored data to this instance's message handler
        to parse and send it to some services like Xively etc.
        '''
        self.post_queue(1, api_frame)

    def _do_post_data_to_service(self, api_frame):
        '''
        _do_post_data_to_service: XBee API frame dictionary -> None

        Parse and send data to some services like Xively etc.
        '''
        got_sensor_info = self.get_senser_data(api_frame)

        now = datetime.datetime.utcnow()
        self._logger.info(now)

        datastreams = []
        for sensor_type in got_sensor_info:
            sensor_value = got_sensor_info[sensor_type]
            datastreams.append(xively.Datastream(
                id=VegetablesPlanterMonitor._XIVELY_ID_TABLE[sensor_type],
                current_value=sensor_value, at=now))

        self._xively_feed.datastreams = datastreams
        self._xively_feed.update()

