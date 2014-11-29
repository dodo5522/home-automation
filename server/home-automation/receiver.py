#!/usr/bin/env python3

"""
 Server side code work on raspberry pi for my home automation.
 Editor     : Takashi Ando
 Version    : 1.0
"""
import logging
from home_automation.base import xbeereceiver
from home_automation.base import config
from home_automation import gardening

class RPiUartReceiver(\
        xbeereceiver.ReceiverProcess,\
        config.Configuration):
    '''
    Process to receive data from XBee.
    There should be only one instance against one XBee coordinator.
    '''

    _ID_START_MONITORS = 0

    def __init__(self, path_to_config, log_level=logging.INFO):
        self._logger = logging.getLogger(type(self).__name__)
        self._logger.setLevel(log_level)

        self._monitors = []

        self._log_level = log_level
        self._path_to_config = path_to_config
        config.Configuration.__init__(self, path_to_config, log_level=log_level)

        self._port = self.read_config('port')
        self._baurate = self.read_config('baurate', int)

        if self._port is None:
            raise ValueError('Serial port is not defined on conf file.')
        if self._baurate is None:
            raise ValueError('Serial baurate is not defined on conf file.')

        xbeereceiver.ReceiverProcess.__init__(self, self._port, self._baurate, log_level=log_level)

        self.append_queue_handler(RPiUartReceiver._ID_START_MONITORS, self._do_start_monitors)

    def start_monitors(self):
        '''
        start_monitors: None -> None

        Start all monitor on the running process.
        If these monitors are started, they would not be the child of newly created process.
        So you need to post this message to start all monitor on newly created process.
        '''
        self.post_queue(self._ID_START_MONITORS)

    def _do_start_monitors(self):
        '''
        start_monitors: None -> None

        This handler would be done if _ID_START_MONITORS is received.
        '''
        self._monitors.append(gardening.VegetablesPlanterMonitor(self._path_to_config, log_level=self._log_level))
        #monitors.append(powerplant.SolarPowerMonitor(arg_parsed.config, log_level=log_level))

        self._logger.info('monitor process objects have been generated.')

        for monitor in self._monitors:
            monitor.start()

        self._init_xbee()

    def _terminate(self):
        '''
        _terminate: None -> None

        Wait for all monitor process joined.
        '''
        for obj in self._monitors:
            obj.post_terminate()
            self._logger.debug('terminating {0}'.format(obj))
            obj.join(30)
            self._logger.info('joined {0}'.format(obj))

        xbeereceiver.ReceiverProcess._terminate(self)

if __name__ == '__main__':
    config_test = []
    config_test.append('[rpiuartreceiver]\n')
    config_test.append('port = /dev/tty0\n')
    config_test.append('baurate = 9600\n')

    fp = open('setting.conf', 'w')
    for line in config_test:
        fp.write(line)
    fp.close()

    #FIXME: dummy monitor instance is needed!
    test_receiver = RPiUartReceiver(RPiUartReceiver, log_level=logging.DEBUG)

    print(test_receiver._port)
    print(test_receiver._baurate)

