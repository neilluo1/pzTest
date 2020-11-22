# !/usr/bin/env python
# -*- coding: utf-8 -*

import threading
from libs.log_obj import LogObj
from utils.util import sleep

logger = LogObj().get_logger()


class Singleton(object):
    def __init__(self, cls):
        self._instance = None
        self._cls = cls
        self._lock = threading.Lock()

    def __call__(self, *args, **kwargs):
        if self._instance is None:
            with self._lock:
                if self._instance is None:
                    self._instance = self._cls(*args, **kwargs)

        return self._instance


def print_for_call(func):
    def wrapper_func(*args, **kwargs):
        logger.debug('Enter {name}.'.format(name=func.__name__))
        rtn = func(*args, **kwargs)
        logger.debug('Exit from {name}. result: {rtn_code}'.format(name=func.__name__, rtn_code=rtn))
        return rtn

    return wrapper_func


def lock(func):
    lock_obj = threading.Lock()

    def wrapper_func(*args, **kwargs):
        with lock_obj:
            rtn = func(*args, **kwargs)

        return rtn

    return wrapper_func


def retry(tries, delay):
    def decorator_func(func):
        def wrapper_func(*args, **kwargs):
            for i in range(1, tries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if i == tries:
                        logger.error('{err}, retry times arrived!({tries}/{total_tries})'.format(err=e, tries=i,
                                                                                                 total_tries=tries))
                        raise e
                    else:
                        logger.warning(
                            '{err}, retrying after {delay} seconds!({tries}/{total_tries})'.format(err=e, delay=delay,
                                                                                                   tries=i,
                                                                                                   total_tries=tries))
                        sleep(delay)

        return wrapper_func

    return decorator_func
