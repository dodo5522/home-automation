#!/usr/bin/env python3

class TerminateProcess(Exception):
    '''Exception to terminate process or thread.
    '''
    pass

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

