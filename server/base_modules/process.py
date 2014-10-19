#!/usr/bin/env python3

"""
 Server side code work on raspberry pi for my home automation.
 Editor     : Takashi Ando
 Version    : 1.0
"""
import multiprocessing
import logging

class BaseProcess(multiprocessing.Process):
    '''Base class to generate process with conmunication by queue messaging.
    '''
    QUEUE_ID_TERMINATE = 0

    def __init__(self, log_level=None):
        '''Initialize process.
           Queue message id 0 is reserved by termination of process.
        '''
        self._logger = logging.getLogger(type(self).__name__)
        self._logger.setLevel(log_level)

        multiprocessing.Process.__init__(self, name=type(self).__name__)

        self._message_queue = multiprocessing.Queue()

        self._message_table = {}
        self._message_table[BaseProcess.QUEUE_ID_TERMINATE] = self._do_terminate

    def run(self):
        '''Parse message queue.
        '''
        while True:
            item = self._message_queue.get()

            queue_id = item[0]
            queue_args = item[1]
            func = self._message_table[queue_id]

            self._logger.debug('got message with id {0} with args {1}.'.format(queue_id, queue_args))

            if queue_args is None:
                func()
            else:
                func(queue_args)

            if queue_id == BaseProcess.QUEUE_ID_TERMINATE:
                break

    def post_queue(self, queue_id, queue_args=None):
        '''Post message to message handler.
        '''
        self._message_queue.put_nowait((queue_id, queue_args))

    def post_terminate(self):
        '''Post message to terminate this process.
           You shoul wait for joined with join() method.
        '''
        self.post_queue(BaseProcess.QUEUE_ID_TERMINATE)

    def _do_terminate(self):
        '''Terminate procedure should be implemented by ingerited class.
        '''
        pass

