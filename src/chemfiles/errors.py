# -*- coding=utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals
import warnings
import chemfiles


class ChemfilesWarning(UserWarning):
    '''Warnigns coming from the Chemfiles C++ runtime'''
    pass


class ChemfilesException(BaseException):
    '''Base class for all Chemfiles exceptions'''
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


# Store a reference to the last logging callback, to preven Python from
# garbage-collecting it.
_CURRENT_CALLBACK = None


def set_warnings_callback(function):
    '''
    Call `function` on every warning event. The callback should take a string
    message and return nothing.
    '''
    from chemfiles.ffi import chfl_warning_callback
    from chemfiles import get_c_library

    def callback(message):
        function(message.decode("utf8"))

    global _CURRENT_CALLBACK
    _CURRENT_CALLBACK = chfl_warning_callback(callback)

    get_c_library().chfl_set_warning_callback(_CURRENT_CALLBACK)


def _set_default_warning_callback():
    set_warnings_callback(
        # We need to set stacklevel=4 to get through the lambda =>
        # adapatator => C++ code => Python binding => user code
        lambda message: warnings.warn(message, ChemfilesWarning, stacklevel=4)
    )
