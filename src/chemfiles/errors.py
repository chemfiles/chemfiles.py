# -*- coding=utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals
import chemfiles


class ChemfilesException(BaseException):
    '''Base class for all Chemfiles exceptions'''
    pass


class ArgumentError(ChemfilesException):
    '''Error in argument type'''
    pass


class NullPointerError(ChemfilesException):
    '''Got a NULL pointer from C!'''
    def __init__(self):
        message = "Got a NULL pointer from C! Today is a bad day."
        super(NullPointerError, self).__init__(message)


class CxxException(ChemfilesException):
    '''Error in the C++ runtime'''
    def __init__(self, status):
        self.status = status
        super(CxxException, self).__init__(last_error())


def last_error():
    '''Get the last error from the library'''
    return chemfiles.get_c_library().chfl_last_error().decode("utf8")


def clear_errors():
    '''Clear any error message saved in the library'''
    return chemfiles.get_c_library().chfl_clear_errors()


def _check_return_code(status, _function, _arguments):
    '''Check that the function call was OK, and raise an exception if needed'''
    if status.value != 0:
        raise CxxException(status)


def _check_handle(handle):
    '''Check that C allocated pointers are not NULL'''
    try:
        handle.contents
    except ValueError:
        raise NullPointerError()
