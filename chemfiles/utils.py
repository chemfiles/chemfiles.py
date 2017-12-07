# -*- coding=utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals
import warnings
from ctypes import create_string_buffer, c_uint64

from .clib import _get_c_library

__all__ = ["ChemfilesError", "set_warnings_callback", "add_configuration"]


class ChemfilesWarning(UserWarning):
    '''Warnings from the Chemfiles runtime.'''
    pass


class ChemfilesError(BaseException):
    '''Exception class for errors in chemfiles'''
    pass


class CxxPointer(object):
    @property
    def ffi(self):
        return _get_c_library()

    @classmethod
    def from_param(cls, parameter):
        if parameter is None:
            raise TypeError("Can not pass None as a " + cls.__name__)
        if not isinstance(parameter, cls):
            raise TypeError(
                "Can not pass " + parameter.__class__.__name__ +
                " as a " + cls.__name__
            )
        return parameter

    def __init__(self, ptr):
        _check_handle(ptr)
        self.ptr = ptr
        self._as_parameter_ = self.ptr

    @classmethod
    def from_ptr(cls, ptr):
        '''

        '''
        new = cls.__new__(cls)
        super(cls, new).__init__(ptr)
        return new


# Store a reference to the last logging callback, to preven Python from
# garbage-collecting it.
_CURRENT_CALLBACK = None


def set_warnings_callback(function):
    '''
    Call `function` on every warning event. The callback should take a string
    message and return nothing.

    By default, warnings are send to python `warnings` module.
    '''
    from .ffi import chfl_warning_callback

    def callback(message):
        try:
            function(message.decode("utf8"))
        except Exception as e:
            message = "exception raised in warning callback: {}".format(e)
            warnings.warn(message, ChemfilesWarning)

    global _CURRENT_CALLBACK
    _CURRENT_CALLBACK = chfl_warning_callback(callback)

    _get_c_library().chfl_set_warning_callback(_CURRENT_CALLBACK)


def add_configuration(path):
    '''
    Read configuration data from the file at ``path``.

    By default, chemfiles reads configuration from any file name `.chemfilesrc`
    in the current directory or any parent directory. This function can be used
    to add data from another configuration file.

    This function will fail if there is no file at ``path``, or if the file is
    incorectly formatted. Data from the new configuration file will overwrite
    any existing data.
    '''
    _get_c_library().chfl_add_configuration(path.encode("utf8"))


def _last_error():
    '''Get the last error from the chemfiles runtime.'''
    return _get_c_library().chfl_last_error().decode("utf8")


def _clear_errors():
    '''Clear any error message saved in the chemfiles runtime.'''
    return _get_c_library().chfl_clear_errors()


def _check_return_code(status, _function, _arguments):
    '''Check that the function call was OK, and raise an exception if needed'''
    if status.value != 0:
        raise ChemfilesError(_last_error())


def _check_handle(handle):
    '''Check that C allocated pointers are not NULL'''
    try:
        handle.contents
    except ValueError:
        raise ChemfilesError(_last_error())


def _set_default_warning_callback():
    set_warnings_callback(
        # We need to set stacklevel=4 to get through the lambda =>
        # adapatator => C++ code => Python binding => user code
        lambda message: warnings.warn(message, ChemfilesWarning, stacklevel=4)
    )


def _call_with_growing_buffer(function, initial):
    '''
    Call ``function`` with a growing buffer until the buffer is big enough.
    Use ``initial`` as the initial buffer size.
    '''
    def buffer_was_big_enough(buffer):
        if len(buffer) < 2:
            return False
        else:
            return buffer[-2] == b'\0'

    size = initial
    buffer = create_string_buffer(b'\0', size)
    function(buffer, c_uint64(size))

    while not buffer_was_big_enough(buffer):
        # Grow the buffer and retry
        size *= 2
        buffer = create_string_buffer(b'\0', size)
        function(buffer, c_uint64(size))

    return buffer.value.decode("utf8")
