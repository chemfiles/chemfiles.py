# -*- coding=utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals
import sys
from ctypes import create_string_buffer, c_uint64

from .clib import _get_c_library
from .misc import ChemfilesError, _last_error


if sys.version_info >= (3, 0):
    string_type = str
else:
    string_type = basestring


class CxxPointer(object):
    __frozen = False
    __ptr = 0

    def __init__(self, ptr, is_const=True):
        self.__ptr = ptr
        self.__is_const = is_const
        self.__frozen = True
        _check_handle(ptr)

    def __del__(self):
        """Free the memory associated with this instance"""
        self.ffi.chfl_free(self.ptr)

    def __setattr__(self, key, value):
        if self.__frozen and not hasattr(self, key):
            raise TypeError(
                "Can not add new attributes to this {}".format(self.__class__.__name__)
            )
        object.__setattr__(self, key, value)

    @classmethod
    def from_mutable_ptr(cls, ptr):
        """Create a new instance from a mutable pointer"""
        new = cls.__new__(cls)
        super(cls, new).__init__(ptr, is_const=False)
        return new

    @classmethod
    def from_const_ptr(cls, ptr):
        """Create a new instance from a const pointer"""
        new = cls.__new__(cls)
        super(cls, new).__init__(ptr, is_const=True)
        return new

    @property
    def mut_ptr(self):
        """Get the **mutable** C++ pointer for this object"""
        if self.__is_const:
            raise ChemfilesError("Trying to use a const pointer for mutable access")
        else:
            return self.__ptr

    @property
    def ptr(self):
        """Get the **const** C++ pointer for this object"""
        return self.__ptr

    @property
    def ffi(self):
        """Allow to access the C interface from any instance of CxxPointer"""
        return _get_c_library()

    @classmethod
    def from_param(cls, parameter):
        if parameter is None:
            raise TypeError("Can not pass None as a " + cls.__name__)
        if not isinstance(parameter, cls):
            raise TypeError(
                "Can not pass " + parameter.__class__.__name__ + " as a " + cls.__name__
            )
        return parameter


def _check_return_code(status, _function, _arguments):
    """Check that the function call was OK, and raise an exception if needed"""
    if status.value != 0:
        raise ChemfilesError(_last_error())


def _check_handle(handle):
    """Check that C allocated pointers are not NULL"""
    try:
        handle.contents
    except ValueError:
        raise ChemfilesError(_last_error())


def _call_with_growing_buffer(function, initial):
    """
    Call ``function`` with a growing buffer until the buffer is big enough.
    Use ``initial`` as the initial buffer size.
    """

    def buffer_was_big_enough(buffer):
        if len(buffer) < 2:
            return False
        else:
            return buffer[-2] == b"\0"

    size = initial
    buffer = create_string_buffer(b"\0", size)
    function(buffer, c_uint64(size))

    while not buffer_was_big_enough(buffer):
        # Grow the buffer and retry
        size *= 2
        buffer = create_string_buffer(b"\0", size)
        function(buffer, c_uint64(size))

    return buffer.value.decode("utf8")
