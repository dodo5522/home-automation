#!/usr/bin/env python3

"""
 Server side code work on raspberry pi for my home automation.
 Editor     : Takashi Ando
 Version    : 1.0
"""
import sys
import argparse
import time
import logging
import gardening
from base_modules import xbeereceiver

LOGGING_FORMAT = '%(asctime)s %(name)-8s %(levelname)-8s: %(message)s'
DATE_FORMAT = '%Y/%m/%d %H:%M:%S'

def init_args(args=None):
    '''
    init_args: args -> argparse.Namespace

    If argv is None, this function takes sys.argv.
    And this function return the parsed argument object.
    '''
    parser = argparse.ArgumentParser(description='Server side script of XBee monitoring system.')

    parser.add_argument('-l', '--log', \
            nargs='?', \
            action='store', \
            default=None, \
            const='/var/log/xbee_monitor.log', \
            required=False, \
            metavar='path_to_log_file', \
            help='Path to log file')
    parser.add_argument('-d', '--debug', \
            action='store_true', \
            default=False, \
            required=False, \
            help='Pint message for debug')

    return parser.parse_args(args)

if __name__ == '__main__':
    arg_parsed = init_args(args=sys.argv[1:])

    if arg_parsed.debug:
        log_level = logging.DEBUG
    else:
        log_level = logging.INFO

    # root logger setting with default Formatter and StreamHandler.
    logging.basicConfig(
        level=log_level,
        format=LOGGING_FORMAT,
        datefmt=DATE_FORMAT)

    # add logging handler of file to root logger.
    if arg_parsed.log is not None:
        formatter = logging.Formatter(fmt=LOGGING_FORMAT, datefmt=DATE_FORMAT)
        handler = logging.FileHandler(arg_parsed.log, mode='a')
        handler.setFormatter(formatter)
        logging.getLogger().addHandler(handler)
        #logging.getLogger().removeHandler(handler)

    logger = logging.getLogger(name=__name__)

    monitors = []
    monitors.append(gardening.VegetablesPlanterMonitor(
        0x0013a20040b44f84,
        'h22...',
        1779591762,
        log_level=log_level))
    #monitors.append(powerplant.SolarPowerMonitor(
    #    0x0013a20040afbcce,
    #    ,
    #    log_level=log_level))

    logger.info('monitor process objects have been generated.')

    receivers = []
    receivers.append(xbeereceiver.ReceiverProcess(
        monitors,
        port=arg_parsed.ports[0],
        log_level=log_level))

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

    for receiver in receivers:
        receiver.post_terminate()
        receiver.join(30)
        logger.info('{PROCESS} is joined.'.format(PROCESS=receiver))

