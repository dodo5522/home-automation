#!/usr/bin/env python3
'''
Unit test code
'''
import os
import unittest
import logging
import datetime,time
from base.process import BaseProcess
from base.xbeereceiver import ReceiverProcess
from base.config import Configuration

def measure_time(func):
    import functools
    import datetime
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = datetime.datetime.today()
        result = func(*args, **kwargs)
        end = datetime.datetime.today()
        return end - start
    return wrapper

class MyUnitTest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_BaseProcess(self):
        wait_time = 4

        class TestChildProcess1(BaseProcess):
            def post_terminate(self):
                self._message_queue.put_nowait((BaseProcess.QUEUE_ID_TERMINATE, wait_time))
                logging.debug('{0}: sleep 10 terminate message is posted.'.format(self.name))

            def _do_terminate(self, wait):
                for i in range(0, wait):
                    logging.debug('{0}: terminating.'.format(self.name))
                    time.sleep(1)
                logging.debug('{0}: terminated.'.format(self.name))

        class TestChildProcess2(BaseProcess):
            def post_terminate(self):
                self._message_queue.put_nowait((BaseProcess.QUEUE_ID_TERMINATE, int(wait_time/2)))
                logging.debug('{0}: sleep 5 terminate message is posted.'.format(self.name))

            def _do_terminate(self, wait):
                for i in range(0, wait):
                    logging.debug('{0}: terminating.'.format(self.name))
                    time.sleep(1)
                logging.debug('{0}: terminated.'.format(self.name))

        p = []
        p.append(TestChildProcess1(log_level=logging.DEBUG))
        p.append(TestChildProcess2(log_level=logging.DEBUG))

        start_time = datetime.datetime.now()
        logging.debug(start_time)

        for process in p:
            process.start()

        # post terminate message to all process
        for process in p:
            process.post_terminate()

        for process in p:
            process.join()

        end_time = datetime.datetime.today()
        logging.debug(end_time)

        diff_seconds = (end_time - start_time).seconds
        diff_seconds += (end_time - start_time).microseconds / 1000000.0
        logging.info('diff: {0} [s]'.format(diff_seconds))

        #TODO: not perfect test pattern...
        self.assertTrue(diff_seconds >= wait_time)
        self.assertTrue(diff_seconds < wait_time + 1)

        for process in p:
            self.assertFalse(process.is_alive())

    def test_ReceiverProcess(self):
        pass

    def test_Configuration(self):
        config_test = []
        config_test.append('[testmonitor]\n')
        config_test.append('value1 = 123\n')
        config_test.append('value2 = abc\n')
        config_test.append('value3 = 0xff\n')

        fp = open('setting.conf', 'w')
        for line in config_test:
            fp.write(line)
        fp.close()

        class TestMonitor(Configuration):
            def __init__(self):
                Configuration.__init__(self, path_to_config=os.path.join(os.getcwd(), 'setting.conf'), log_level=logging.DEBUG)
            def read_value1(self):
                return self.read_config('value1', int)
            def read_value2(self):
                return self.read_config('value2')
            def read_value3(self):
                return self.read_config('value3', int, 16)

        sample_monitor = TestMonitor()
        self.assertEqual(sample_monitor.read_value1(), 123)
        self.assertEqual(sample_monitor.read_value2(), 'abc')
        self.assertEqual(sample_monitor.read_value3(), 255)

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()

