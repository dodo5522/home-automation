#!/usr/bin/env python3

"""
 Server side code work on raspberry pi for my home automation.
 Editor     : Takashi Ando
 Version    : 1.0
"""
import multiprocessing
import queue
import logging

class BaseProcess(multiprocessing.Process):
    '''Base class to generate process with conmunication by queue messaging.
    '''
    _ID_TERMINATE_PROCESS = -1

    def __init__(self, log_level=None):
        '''Initialize process.
           Queue message id 0 is reserved by termination of process.
        '''
        self._logger = logging.getLogger(type(self).__name__)
        self._logger.setLevel(log_level)

        multiprocessing.Process.__init__(self, name=type(self).__name__)

        self._message_queue = multiprocessing.Queue()
        self._message_table = {}

        self._running = False

    def run(self):
        '''Parse message queue.
        '''
        self._running = True

        while self._running:
            try:
                item = self._message_queue.get(block=True, timeout=3)

            except queue.Empty:
                continue

            else:
                queue_id = item[0]
                queue_args = item[1]

                self._logger.debug('got message with id {0} with args {1}.'.format(queue_id, queue_args))

                if queue_id == BaseProcess._ID_TERMINATE_PROCESS:
                    self._terminate()
                elif queue_id not in self._message_table:
                    raise NotImplementedError("Handler atainst ID does not exist.")
                else:
                    func = self._message_table[queue_id]
                    if queue_args is None:
                        func()
                    else:
                        func(queue_args)

    def post_queue(self, queue_id, queue_args=None):
        '''Post message to message handler.
        '''
        self._message_queue.put_nowait((queue_id, queue_args))

    def post_terminate(self):
        '''Post message to terminate this process.
           You shoul wait for joined with join() method.
        '''
        self.post_queue(BaseProcess._ID_TERMINATE_PROCESS)

    def append_queue_handler(self, queue_id, handler):
        '''
        append_queue_handler: None -> None

        Add new handler against the queue ID.
        If there is the handler against ID, raise ValueError.
        '''
        if queue_id in self._message_table:
            raise ValueError("The ID {0} is already set.".format(queue_id))

        self._message_table[queue_id] = handler

    def _terminate(self):
        '''
        _terminate: None -> None

        This function is called after break queue handler loop.
        This function should be implemented to close all instance used in this process.
        '''
        self._running = False

