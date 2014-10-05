#!/usr/bin/env python3

"""
 Server side code work on raspberry pi for my home automation.
 Editor     : Takashi Ando
 Version    : 1.0
"""
import logging
import xbeereceiver
import gardening

LOGGING_FORMAT_BASIC = '%(asctime)s %(name)-8s %(levelname)-8s: %(message)s'
LOGGING_FORMAT_DATE = '%Y/%m/%d %H:%M:%S'

if __name__ == '__main__':
    # root logger setting with default Formatter and StreamHandler.
    logging.basicConfig(level=logging.INFO,
            format=LOGGING_FORMAT_BASIC,
            datefmt=LOGGING_FORMAT_DATE)

    # add logging handler of file to root logger.
    formatter = logging.Formatter(fmt=LOGGING_FORMAT_BASIC, datefmt=LOGGING_FORMAT_DATE)
    handler = logging.FileHandler('/tmp/test.log', mode='a')
    handler.setFormatter(formatter)
    logging.getLogger().addHandler(handler)
    #logging.getLogger().removeHandler(handler)

    main_logger = logging.getLogger(name=__name__)

    monitors = []
    monitors.append(gardening.GardeningMonitor())

    for process in monitors:
        process.run()

    while True:
        receiver = xbeereceiver.XBeeReceiver()
        receiver.wait_for_api_frame()

    for process in monitors:
        process.join()

