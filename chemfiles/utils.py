# -*- coding=utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals
import sys

import ctypes
from ctypes import create_string_buffer, c_uint64, pointer

from typing import Optional, Callable, Any, Type, TypeVar

from .clib import _get_c_library
from .misc import ChemfilesError, _last_error


if sys.version_info >= (3, 0):
    string_type = str
else:
    string_type = basestring  # noqa


CxxPtrChild = TypeVar("CxxPtrChild", bound="CxxPointer")


class CxxPointer(object):
    # Used to prevent adding new attributes to chemfiles objects
    __frozen = False
    # C++ allocated pointer
    __ptr = None  # type: pointer[Any]
    # Is the C++ pointer a const pointer? This is required since const and
    # non-const pointers have the same ABI, but modifying an object through
    # a const pointer is UB and should be prevented
    __is_const = False
    # None for newly allocated objects, or a CxxPointer instance for objects
    # living inside another object (typically atoms inside a frame, or
    # residue in a topology).
    __origin = None

    def __init__(self, ptr, is_const=True, origin=None):
        # type: (pointer[Any], bool, Optional[Any]) -> None
        self.__ptr = ptr
        self.__is_const = is_const
        self.__origin = origin
        self.__frozen = True
        _check_handle(ptr)

    def __del__(self):
        # type: () -> None
        """Free the memory associated with this instance"""
        self.ffi.chfl_free(self.ptr)

    def __setattr__(self, key, value):
        # type: (Any, Any) -> None
        if self.__frozen and not hasattr(self, key):
            raise TypeError(
                "Can not add new attributes to this {}".format(self.__class__.__name__)
            )
        object.__setattr__(self, key, value)

    @classmethod
    def from_mutable_ptr(cls, origin, ptr):
        # type: (Type[CxxPtrChild], Optional[Any], pointer[Any]) -> CxxPtrChild
        """Create a new instance from a mutable pointer"""
        new = cls.__new__(cls)  # type: CxxPtrChild
        CxxPointer.__init__(new, ptr, is_const=False, origin=origin)
        return new

    @classmethod
    def from_const_ptr(cls, origin, ptr):
        # type: (Type[CxxPtrChild], Optional[Any], pointer[Any]) -> CxxPtrChild
        """Create a new instance from a const pointer"""
        new = cls.__new__(cls)  # type: CxxPtrChild
        CxxPointer.__init__(new, ptr, is_const=True, origin=origin)
        return new

    @property
    def mut_ptr(self):
        # type: () -> pointer[Any]
        """Get the **mutable** C++ pointer for this object"""
        if self.__is_const:
            raise ChemfilesError(
                "Trying to use a const pointer for mutable access, this is a bug"
            )
        else:
            return self.__ptr

    @property
    def ptr(self):
        # type: () -> pointer[Any]
        """Get the **const** C++ pointer for this object"""
        return self.__ptr

    @property
    def ffi(self):
        # type: () -> ctypes.CDLL
        """Allow to access the C interface from any instance of CxxPointer"""
        return _get_c_library()

    @classmethod
    def from_param(cls, parameter):
        # type: (Any) -> Any
        if parameter is None:
            raise TypeError("Can not pass None as a " + cls.__name__)
        if not isinstance(parameter, cls):
            raise TypeError(
                "Can not pass " + parameter.__class__.__name__ + " as a " + cls.__name__
            )
        return parameter


def _check_handle(handle):
    # type: (pointer[Any]) -> None
    """Check that C allocated pointers are not NULL"""
    if not handle:
        raise ChemfilesError(_last_error())


def _call_with_growing_buffer(function, initial):
    # type: (Callable[[ctypes.Array[ctypes.c_char], c_uint64], Any], int) -> str
    """
    Call ``function`` with a growing buffer until the buffer is big enough.
    Use ``initial`` as the initial buffer size.
    """

    def buffer_was_big_enough(buffer):
        # type: (ctypes.Array[ctypes.c_char]) -> bool
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
