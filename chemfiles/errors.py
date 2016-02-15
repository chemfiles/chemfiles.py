# -*- coding=utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals
from ctypes import c_int

import chemfiles


class ChemfilesException(BaseException):
    '''Base class for all Chemfiles exceptions'''
    pass


class ArgumentError(ChemfilesException):
    '''Error in argument type'''
    pass


class NullPointerError(ChemfilesException):
    '''Got a NULL pointer from C!'''
    def __init__(self, message=""):
        m = "Got a NULL pointer from C! Today is a bad day."
        if message:
            m += " " + message
        super(NullPointerError, self).__init__(m)


class CPPException(ChemfilesException):
    '''Error in C++ runtime'''
    CPP_STD_ERROR = 1
    CHEMHARP_CPP_ERROR = 2
    MEMORY_ERROR = 3
    FILE_ERROR = 4
    FORMAT_ERROR = 5

    def __init__(self, status):
        self.status = status
        if (status == CPPException.CPP_STD_ERROR or
                status == CPPException.CHEMHARP_CPP_ERROR):
            message = last_error()
        else:
            message = chemfiles.get_c_library().chfl_strerror(c_int(status))
            message = message.decode("utf8")
        super(CPPException, self).__init__(message)


def last_error():
    return chemfiles.get_c_library().chfl_last_error().decode("utf8")


def _check_return_code(result, func, arguments):
    '''Check that the function call was OK, and raise an exception if needed'''
    if result != 0:
        raise CPPException(result)


def _check_handle(handle):
    '''Check that C allocated pointers are not NULL'''
    try:
        handle.contents
    except ValueError:
        raise NullPointerError()
