#!/usr/bin/env python3

"""
 Server side code work on raspberry pi for my home automation.
 Editor     : Takashi Ando
 Version    : 1.0
"""
import time
import logging
import gardening
from base_modules import xbeereceiver

LOGGING_FORMAT = '%(asctime)s %(name)-8s %(levelname)-8s: %(message)s'
DATE_FORMAT = '%Y/%m/%d %H:%M:%S'

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
        0x0013a20040b44f84,
        'h22...',
        1779591762))
    #monitors.append(powerplant.SolarPowerMonitor(
    #    0x0013a20040afbcce,
    #    ,
    #    ))

    logger.info('monitor process objects have been generated.')

    receivers = []
    receivers.append(xbeereceiver.ReceiverProcess(
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

    for receiver in receivers:
        receiver.terminate()
        receiver.join(30)
        logger.info('{PROCESS} is joined.'.format(PROCESS=receiver))

