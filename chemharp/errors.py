# -*- coding=utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals
from ctypes import c_int

import chemharp


class ChemharpException(BaseException):
    '''Base class for all Chemharp exceptions'''
    pass


class ArgumentError(ChemharpException):
    '''Error in argument type'''
    pass


class NullPointerError(ChemharpException):
    '''Got a NULL pointer from C!'''
    def __init__(self, message=""):
        m = "Got a NULL pointer from C! Today is a bad day."
        if message:
            m += " " + message
        super(NullPointerError, self).__init__(m)


class CPPException(ChemharpException):
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
            message = chemharp.ffi.c_lib.chrp_strerror(c_int(status))
            message = message.decode("utf8")
        super(CPPException, self).__init__(message)


def last_error():
    return chemharp.ffi.c_lib.chrp_last_error().decode("utf8")


def _check(result, func, arguments):
    '''Check that the function call was OK, and raise an exception if needed'''
    if result != 0:
        raise CPPException(result)


def _check_handle(handle):
    '''Check that C allocated pointers are not NULL'''
    try:
        handle.contents
    except ValueError:
        raise NullPointerError()
