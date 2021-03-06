#!/usr/bin/env python3
'''
Unit test code
'''
import os
import unittest
import logging
import datetime,time
from home_automation.base.process import BaseProcess
from home_automation.base.xbeereceiver import ReceiverProcess
from home_automation.base.config import Configuration
from home_automation.base.tweet import Twitter

class TwitterTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.CONSUMER_KEY = ""
        cls.CONSUMER_SEC = ""
        cls.ACCESS_TOK = ""
        cls.ACCESS_SEC = ""

        cls.OBJ = Twitter(\
                cls.CONSUMER_KEY, \
                cls.CONSUMER_SEC, \
                cls.ACCESS_TOK, \
                cls.ACCESS_SEC)

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @unittest.skip("cannot test this yet.")
    def test_tweet(self):
        self.assertTrue(self.OBJ.tweet("test message."))

class BaseProcessTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_BaseProcess(self):
        class TestChildProcess1(BaseProcess):
            pass

        class TestChildProcess2(BaseProcess):
            pass

        p = []
        p.append(TestChildProcess1(log_level=logging.DEBUG))
        p.append(TestChildProcess2(log_level=logging.DEBUG))

        start_time = datetime.datetime.now()
        logging.debug(start_time)

        for process in p:
            process.start()

        for process in p:
            self.assertTrue(process.is_alive())

        for process in p:
            process.post_terminate()

        for process in p:
            process.join(1)

        for process in p:
            self.assertFalse(process.is_alive())

        end_time = datetime.datetime.today()
        logging.debug(end_time)

        diff_seconds = (end_time - start_time).seconds
        diff_seconds += (end_time - start_time).microseconds / 1000000.0
        logging.info('diff: {0} [s]'.format(diff_seconds))

class ReceiverProcessTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @unittest.skip("not yet implemented")
    def test_ReceiverProcess(self):
        raise NotImplementedError

class ConfigurationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
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

