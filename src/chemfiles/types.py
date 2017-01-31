# -*- coding=utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

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
