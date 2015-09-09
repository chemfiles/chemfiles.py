# -*- coding=utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals
from enum import IntEnum
from ctypes import c_int, byref

from .ffi import get_c_library, CHRP_LOG_LEVEL


class LogLevel(IntEnum):
    '''
    Available log levels:
        - NONE: Do not log anything
        - ERROR: Only log errors
        - WARNING: Log errors and warnings
        - INFO: Log errors, warnings and informations
        - DEBUG: Log everything, from errors to debug informations
    '''
    NONE = CHRP_LOG_LEVEL.CHRP_LOG_NONE
    ERROR = CHRP_LOG_LEVEL.CHRP_LOG_ERROR
    WARNING = CHRP_LOG_LEVEL.CHRP_LOG_WARNING
    INFO = CHRP_LOG_LEVEL.CHRP_LOG_INFO
    DEBUG = CHRP_LOG_LEVEL.CHRP_LOG_DEBUG


def log_level():
    '''Get current logging level'''
    c_lib = get_c_library()
    res = c_int()
    c_lib.chrp_loglevel(byref(res))
    return LogLevel(res.value)


def set_log_level(level):
    ''' Set the logging level to ``level``'''
    c_lib = get_c_library()
    c_lib.chrp_set_loglevel(c_int(level))


def log_to_file(path):
    '''Write logs to the file at ``path``, creating it if needed.'''
    c_lib = get_c_library()
    c_lib.chrp_logfile(path.encode("utf8"))


def log_to_stderr():
    '''Write logs to the standard error stream. This is the default.'''
    c_lib = get_c_library()
    c_lib.chrp_log_stderr()
