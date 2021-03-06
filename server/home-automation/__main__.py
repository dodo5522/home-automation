#!/usr/bin/env python3

"""
 Server side code work on raspberry pi for my home automation.
 Editor     : Takashi Ando
 Version    : 1.0
"""
import argparse
import time
import logging
import signal
from home_automation import receiver

LOGGING_FORMAT = '%(asctime)s %(name)-8s %(levelname)-8s: %(message)s'
DATE_FORMAT = '%Y/%m/%d %H:%M:%S'

RUNNING = True

def stop(signum, frame):
    '''
    stop:None -> None

    stop main loop function which is called by signal handler.
    '''
    global RUNNING
    RUNNING = False

def main():
    '''
    main:None -> None

    main loop function.
    '''
    parser = argparse.ArgumentParser(description='Server side script of XBee monitoring system.')
    parser.add_argument('-c', '--config', \
            action='store', \
            default='/etc/home_automation/setting.conf', \
            required=False, \
            metavar='path_to_conf_file', \
            help='Path to config file')
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

    arg_parsed = parser.parse_args()

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

    receivers = []
    receivers.append(receiver.RPiUartReceiver(arg_parsed.config, log_level=log_level))
    #receivers.append(receiver.UsbSerReceiver(arg_parsed.config, log_level=log_level))

    logger.info('receiver proces objects have been generated.')

    for obj in receivers:
        obj.start()
        obj.start_monitors()

    logger.info('all receiver process has started.')

    while RUNNING:
        #FIXME: check if all receiver process is alive or not.
        logger.debug('sleeping...')
        time.sleep(3)

    for obj in receivers:
        obj.post_terminate()
        logger.debug('terminating {0}'.format(obj))
        obj.join(30)
        logger.info('joined {0}'.format(obj))

if __name__ == '__main__':
    signal.signal(signal.SIGINT, stop)
    signal.signal(signal.SIGTERM, stop)
    main()

