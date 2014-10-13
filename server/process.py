#!/usr/bin/env python3

"""
 Server side code work on raspberry pi for my home automation.
 Editor     : Takashi Ando
 Version    : 1.0
"""
import multiprocessing
import logging

class BaseProcess(multiprocessing.Process):
    '''Base class to generate process.
    '''
    def __init__(self, log_level=None):
        '''Initialize process.
        '''
        self._logger = logging.getLogger(type(self).__name__)
        self._logger.setLevel(log_level)

        multiprocessing.Process.__init__(self, name=type(self).__name__)

        self._message_queue = multiprocessing.Queue()

        self._message_table = {}
        self._message_table[0] = self._do_terminate

    def run(self):
        '''Parse message queue.
        '''
        while True:
            item = self._message_queue.get()
            self._logger.debug('got message id {0}.'.format(item[0]))

            func = self._message_table[item[0]]
            if item[1] is None:
                func()
            else:
                func(item[1])

            # id 0 means termination.
            if item[0] == 0:
                break

    def terminate(self):
        '''Post message to terminate this process.
           You shoul wait for joined with join() method.
        '''
        self._message_queue.put_nowait((0, None))

    def _do_terminate(self):
        '''Terminate procedure should be implemented.
        '''
        raise NotImplementedError

if __name__ == '__main__':
    import time

    class TestChildProcess1(BaseProcess):
        def terminate(self):
            self._message_queue.put_nowait((0, 10))
            print('{0}: sleep 10 terminate message is posted.'.format(self.name))

        def _do_terminate(self, wait):
            for i in range(0, wait):
                print('{0}: terminating.'.format(self.name))
                time.sleep(1)
            print('{0}: terminated.'.format(self.name))

    class TestChildProcess2(BaseProcess):
        def terminate(self):
            self._message_queue.put_nowait((0, 5))
            print('{0}: sleep 5 terminate message is posted.'.format(self.name))

        def _do_terminate(self, wait):
            for i in range(0, wait):
                print('{0}: terminating.'.format(self.name))
                time.sleep(1)
            print('{0}: terminated.'.format(self.name))

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

