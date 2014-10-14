#!/usr/bin/env python3
'''
Unit test code
'''

import unittest
import logging
from base_modules.process import BaseProcess

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    import time
    class TestChildProcess1(BaseProcess):
        def terminate(self):
            self._message_queue.put_nowait((0, 10))
            logging.debug('{0}: sleep 10 terminate message is posted.'.format(self.name))

        def _do_terminate(self, wait):
            for i in range(0, wait):
                logging.debug('{0}: terminating.'.format(self.name))
                time.sleep(1)
            logging.debug('{0}: terminated.'.format(self.name))

    class TestChildProcess2(BaseProcess):
        def terminate(self):
            self._message_queue.put_nowait((0, 5))
            logging.debug('{0}: sleep 5 terminate message is posted.'.format(self.name))

        def _do_terminate(self, wait):
            for i in range(0, wait):
                logging.debug('{0}: terminating.'.format(self.name))
                time.sleep(1)
            logging.debug('{0}: terminated.'.format(self.name))

    p = []
    p.append(TestChildProcess1(log_level=logging.DEBUG))
    p.append(TestChildProcess2(log_level=logging.DEBUG))

    for process in p:
        process.start()

    # post terminate message to all process
    for process in p:
        process.terminate()

    for process in p:
        process.join()

