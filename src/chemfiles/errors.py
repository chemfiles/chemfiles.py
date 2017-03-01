# -*- coding=utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals
import warnings
import chemfiles


class ChemfilesWarning(UserWarning):
    '''Warnings coming from the Chemfiles runtime.'''
    pass


class ChemfilesException(BaseException):
    '''Error in the chemfiles runtime.'''
    def __init__(self, status=None, message=""):
        self.status = status
        if message == "":
            message = last_error()
        super(ChemfilesException, self).__init__(message)


def last_error():
    '''Get the last error from the chemfiles runtime.'''
    return chemfiles.get_c_library().chfl_last_error().decode("utf8")


def clear_errors():
    '''Clear any error message saved in the chemfiles runtime.'''
    return chemfiles.get_c_library().chfl_clear_errors()


def _check_return_code(status, _function, _arguments):
    '''Check that the function call was OK, and raise an exception if needed'''
    if status.value != 0:
        raise ChemfilesException(status=status)


def _check_handle(handle):
    '''Check that C allocated pointers are not NULL'''
    try:
        handle.contents
    except ValueError:
        raise ChemfilesException(
            message="Got a NULL pointer from the chemfiles runtime."
        )


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
