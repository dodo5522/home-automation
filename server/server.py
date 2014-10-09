#!/usr/bin/env python3

"""
 Server side code work on raspberry pi for my home automation.
 Editor     : Takashi Ando
 Version    : 1.0
"""
import multiprocessing
import serial
import time
import logging
import gardening
from xbee import ZigBee

LOGGING_FORMAT = '%(asctime)s %(name)-8s %(levelname)-8s: %(message)s'
DATE_FORMAT = '%Y/%m/%d %H:%M:%S'

class ReceiverProcess(multiprocessing.Process):
    '''
    Base class of process to receive data from XBee ZB.
    There should be only one instance against one XBee coordinator.
    '''
    def __init__(self, monitors, port='/dev/ttyAMA0', baurate=9600, log_level=logging.INFO):
        '''
        Initialize XBee instance with serial port and baurate.
        The baurate should be set to same value with XBee module.
        '''
        self._logger = logging.getLogger(type(self).__name__)
        self._logger.setLevel(log_level)

        self._port = port
        self._baurate = baurate
        self._ser = serial.Serial(self._port, self._baurate)
        self._xbee = ZigBee(self._ser, escaped=True)

        self._monitors = monitors

    def run(self):
        '''
        Wait for API frame from XBee module.
        And return the node information (source address etc.) and another data.
        '''
        for monitor in self._monitors:
            monitor.start()

        while True:
            try:
                api_frame = self._xbee.wait_read_frame()
                for monitor in self._monitors:
                    monitor.parse(api_frame)
            except Exception as err:
                print('{0} occurs.'.format(err))
                continue

        for monitor in self._monitors:
            monitor.join()

        # halt() must be called before closing the serial
        # port in order to ensure proper thread shutdown
        if self._xbee is not None:
            self._xbee.halt()
        self._ser.close()

if __name__ == '__main__':
    # root logger setting with default Formatter and StreamHandler.
    logging.basicConfig(
        level=logging.INFO,
        format=LOGGING_FORMAT,
        datefmt=DATE_FORMAT)

    # add logging handler of file to root logger.
    formatter = logging.Formatter(fmt=LOGGING_FORMAT, datefmt=DATE_FORMAT)
    handler = logging.FileHandler('/tmp/test.log', mode='a')
    handler.setFormatter(formatter)
    logging.getLogger().addHandler(handler)
    #logging.getLogger().removeHandler(handler)

    logger = logging.getLogger(name=__name__)

    monitors = []
    monitors.append(gardening.VegetablesPlanterMonitor(
        source_addr_long=0x0013a20040b44f84,
        xively_api_key='h22...',
        xively_feed_id=1779591762))
    #monitors.append(powerplant.SolarPowerMonitor(
    #    source_addr_long=0x0013a20040afbcce,
    #    xively_api_key=,
    #    xively_feed_id=))

    logger.info('monitor process objects have been generated.')

    receivers = []
    receivers.append(ReceiverProcess(
        monitors,
        port='/dev/ttyAMA0'))

    logger.info('receiver proces objects have been generated.')

    for receiver in receivers:
        receiver.start()

    logger.info('all receiver process has started.')

    while True:
        try:
            #FIXME: check if all receiver process is alive or not.
            time.sleep(10)
        except KeyboardInterrupt:
            break
        else:
            #FIXME: check this implementation.
            logger.info('another exception?')
            continue

    for process in receivers:
        process.join()
        logger.info('{PROCESS} is joined.'.format(PROCESS=process))

