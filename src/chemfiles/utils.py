# -*- coding=utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals
from ctypes import create_string_buffer, c_uint64

from chemfiles import get_c_library
from chemfiles.errors import _check_handle


class CxxPointer(object):
    ffi = get_c_library()

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


def call_with_growing_buffer(function, initial):
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
