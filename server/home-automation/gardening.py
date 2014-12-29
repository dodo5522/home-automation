#!/usr/bin/env python3

"""
 Server side code for my gardening.
 Editor     : Takashi Ando
 Version    : 1.0
"""

import xively
import datetime
import logging
from home_automation.base import process
from home_automation.base import xbeeparser
from home_automation.base import config
from home_automation.base import tweet

class Sensor(object):
    def __init__(self, id_arduino, id_xively, value_prev=None, value_next=None):
        self.sensor_data = {}
        self.sensor_data["ID_ARDUINO"] = id_arduino
        self.sensor_data["ID_XIVELY"] = id_xively
        self.sensor_data["VALUE_PREV"] = value_prev
        self.sensor_data["VALUE_NEXT"] = value_next

    def __getitem__(self, key):
        return self.sensor_data[key]

    def __setitem__(self, key, value):
        self.sensor_data[key] = value

class Luminosity(Sensor):
    def __init__(self):
        Sensor.__init__(self, 'LUX0', 'Luminosity')

class Humidity(Sensor):
    def __init__(self):
        Sensor.__init__(self, 'HUM0', 'Humidity')

class MoistureOfSmallPlant(Sensor):
    def __init__(self):
        Sensor.__init__(self, 'MOI0', 'MoistureOfSmallPlant')

class MoistureOfLargePlant(Sensor):
    def __init__(self):
        Sensor.__init__(self, 'MOI1', 'MoistureOfLargePlant')

class Temperature(Sensor):
    def __init__(self):
        Sensor.__init__(self, 'TMP0', 'Temperature')

class VegetablesPlanterMonitor(\
        process.BaseProcess,
        xbeeparser.XBeeApiRfDataParser,
        config.Configuration,
        tweet.Twitter):
    '''
    This class monitors gardening status with XBee.
    And put the information to Xively.
    '''
    _ID_POST_TO_SERVICE = 0

    _SENSORS = \
    [
        Luminosity(),
        Humidity(),
        MoistureOfSmallPlant(),
        MoistureOfLargePlant(),
        Temperature(),
    ]

    def __init__(self, path_to_config, log_level=logging.INFO):
        '''
        Initialize process etc.
        '''
        config.Configuration.__init__(self, path_to_config, log_level=log_level)
        process.BaseProcess.__init__(self, log_level=log_level)
        xbeeparser.XBeeApiRfDataParser.__init__(self, \
                sensors=len(VegetablesPlanterMonitor._SENSORS), \
                log_level=log_level)

        self.append_queue_handler(self._ID_POST_TO_SERVICE, self._do_post_data_to_service)

        api_key = self.read_config('xively_api_key')
        feed_id = self.read_config('xively_feed')

        if api_key == None:
            raise ValueError('Xively API key is not defined on conf file.')
        if feed_id == None:
            raise ValueError('Xively feed ID is not defined on conf file.')

        api = xively.XivelyAPIClient(api_key)
        self._xively_feed = api.feeds.get(feed_id)

        consumer_key = self.read_config('twitter_consumer_key')
        consumer_sec = self.read_config('twitter_consumer_sec')
        access_tok   = self.read_config('twitter_access_tok')
        access_sec   = self.read_config('twitter_access_sec')

        for key in (consumer_key, consumer_sec, access_tok, access_sec):
            if key is None:
                return

        tweet.Twitter(self, consumer_key, consumer_sec, access_tok, access_sec)

    def get_monitoring_address(self):
        '''
        get_monitoring_address: None -> int

        Get XBee 64bit source address to monitor in this instance.
        '''
        return self.read_config('address', int, 16)

    def post_data_to_service(self, api_frame):
        '''
        post_data_to_service: XBee API frame dictionary -> None

        Post monitored data to this instance's message handler
        to parse and send it to some services like Xively etc.
        '''
        self.post_queue(self._ID_POST_TO_SERVICE, api_frame)

    def _do_post_data_to_service(self, api_frame):
        '''
        _do_post_data_to_service: XBee API frame dictionary -> None

        Parse and send data to some services like Xively etc.
        '''
        got_sensor_info = self.get_senser_data(api_frame)

        now = datetime.datetime.utcnow()
        self._logger.info('post sensor data at {0}.'.format(now))

        datastreams = []
        for sensor in self._SENSORS:
            try:
                sensor_value = got_sensor_info[sensor["ID_ARDUINO"]]
            except KeyError:
                continue

            sensor["VALUE_PREV"], sensor["VALUE_NEXT"] = sensor["VALUE_NEXT"], sensor_value

            datastreams.append(xively.Datastream(
                id=sensor["ID_XIVELY"],
                current_value=sensor_value, at=now))

        self._xively_feed.datastreams = datastreams
        self._xively_feed.update()

    def tweet_auto(self, message_table=None, values=()):
        """ Tweet with the specified message.

        Args:
            message_table (dict) : message table with message, direction, and threshold
            values (list) : values[0] is previous value to see the threshold
                            values[1] is next value to see the threshold

            message table should have the below structure.
            message_table = (
                {"enough wet.", "threshold":70, "direction":1},
                {"getting dry.", "threshold":50, "direction":-1},
                {"dangerously dry...", "threshold":30, "direction":-1},
                {"help me...!", "threshold":10, "direction":-1},
                )

        Returns:
            True if succeeded.
        """
        if message_table is not None and len(values) >= 2:
            return self.tweet(message)

        return False

