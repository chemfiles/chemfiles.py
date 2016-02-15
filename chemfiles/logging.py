# -*- coding=utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals
from enum import IntEnum
from ctypes import c_int, byref

from chemfiles import get_c_library
from chemfiles.ffi import CHFL_LOG_LEVEL, chfl_logging_callback_t


class LogLevel(IntEnum):
    '''
    Available log levels:
        - ERROR: Only log errors
        - WARNING: Log errors and warnings
        - INFO: Log errors, warnings and informations
        - DEBUG: Log everything, from errors to debug informations
    '''
    ERROR = CHFL_LOG_LEVEL.CHFL_LOG_ERROR
    WARNING = CHFL_LOG_LEVEL.CHFL_LOG_WARNING
    INFO = CHFL_LOG_LEVEL.CHFL_LOG_INFO
    DEBUG = CHFL_LOG_LEVEL.CHFL_LOG_DEBUG


def log_level():
    '''Get current logging level'''
    c_lib = get_c_library()
    res = c_int()
    c_lib.chfl_loglevel(byref(res))
    return LogLevel(res.value)


def set_log_level(level):
    ''' Set the logging level to ``level``'''
    c_lib = get_c_library()
    c_lib.chfl_set_loglevel(c_int(level))


def log_to_file(path):
    '''Write logs to the file at ``path``, creating it if needed.'''
    c_lib = get_c_library()
    c_lib.chfl_logfile(path.encode("utf8"))


def log_to_stderr():
    '''Write logs to the standard error stream. This is the default.'''
    c_lib = get_c_library()
    c_lib.chfl_log_stderr()


def log_to_stdout():
    '''Write logs to the standard error stream. This is the default.'''
    c_lib = get_c_library()
    c_lib.chfl_log_stdout()


def silent():
    '''Write logs to the standard error stream. This is the default.'''
    c_lib = get_c_library()
    c_lib.chfl_log_silent()

# Store a reference to the last logging callback, to preven Python from
# garbage-collecting it.
_CURRENT_CALLBACK = None


def _wrap_callback(function):
    def callback(level, message):
        function(LogLevel(level.value), message)

    global _CURRENT_CALLBACK
    _CURRENT_CALLBACK = chfl_logging_callback_t(callback)
    return _CURRENT_CALLBACK


def log_callback(callback):
    '''
    Use a callback for logging, instead of the built-in logging system.

    The ``callback`` function must have the following signature:
        def callback(level, message):
            ...
            return None
    where ``level`` is a ``LogLevel``, and message a string containing the log
    message.
    '''
    c_lib = get_c_library()
    c_lib.chfl_log_callback(_wrap_callback(callback))
