#!/usr/bin/env python3

"""
 Server side code work on raspberry pi for my home automation.
 Editor     : Takashi Ando
 Version    : 1.0
"""
import multiprocessing
import logging

class BaseProcess(multiprocessing.Process):
    '''
    Base class to generate process.
    '''
    def __init__(self, log_level=None):
        '''
        Initialize process.
        '''
        self._logger = logging.getLogger(type(self).__name__)
        self._logger.setLevel(log_level)

        multiprocessing.Process.__init__(self, name=type(self).__name__)

        self._message_queue = multiprocessing.Queue()

        self._message_table = {}
        self._message_table[0] = self._do_terminate

    def run(self):
        '''
        Message handler.
        '''
        while True:
            item = self._message_queue.get()
            self._logger.debug('got message id {0}.'.format(item[0]))
            print('got message id {0}.'.format(item[0]))

            func = self._message_table[item[0]]
            if item[1] is None:
                func()
            else:
                func(item[1])

            if item[0] == 0:
                break

    def terminate(self):
        '''
        Post message to terminate this process.
        You should wait for joined with join() method.
        '''
        self._message_queue.put((0, None))

    def _do_terminate(self):
        '''
        Terminate internally.
        '''
        #raise NotImplementedError
        print('terminate internally.')

if __name__ == '__main__':
    p = BaseProcess(log_level=logging.DEBUG)
    p.start()
    p.terminate()
    p.join()

