#!/usr/bin/env python3

"""
 Server side code work on raspberry pi for my home automation.
 Editor     : Takashi Ando
 Version    : 1.0
"""
import logging
import xbeereceiver
import gardening

if __name__ == '__main__':
    # Do other stuff in the main thread
    log_format = '%(asctime)-15s %(module)-8s %(message)s'
    logging.basicConfig(format=log_format)

    monitors = []
    monitors.append(gardening.GardeningMonitor())

    for process in monitors:
        process.run()

    while True:
        receiver = xbeereceiver.XBeeReceiver()
        receiver.wait_for_api_frame()

    for process in monitors:
        process.join()

