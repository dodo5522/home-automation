#!/usr/bin/env python3

"""
 Server side code for my gardening.
 Editor     : Takashi Ando
 Version    : 1.0
"""

import time
import multiprocessing
import logging
import xbeereceiver
import basemonitor

class VegetablesPlanterMonitor(
        multiprocessing.Process,
        xbeereceiver.XBeeApiRfDataParser,
        basemonitor.BaseMonitor):
    '''
    This class monitors gardening status with XBee.
    And put the information to Xively.
    '''
    def __init__(self, source_addr_long=None,\
            xively_api_key=None, xively_feed_id=None,\
            log_level=logging.INFO):
        '''
        Initialize process etc.
        '''
        multiprocessing.Process.__init__(self, name=type(self).__name__)

        basemonitor.BaseMonitor(self,
                source_addr_long=source_addr_long,
                xively_api_key=xively_api_key,
                xively_feed_id=xively_feed_id,
                log_level=log_level)

    def run(self):
        '''
        Method to be run in sub-process; can be overridden in sub-class
        '''
        while True:
            try:
                pass
            except KeyboardInterrupt:
                break
            except Exception as err:
                print('{0} occurs.'.format(err))
                time.sleep(600)
                continue

