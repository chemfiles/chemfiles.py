# -*- coding=utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals
import sys
import numpy as np
from ctypes import c_double, c_bool

from .ffi import chfl_property_kind, chfl_vector3d
from .utils import CxxPointer, _call_with_growing_buffer
from .utils import ChemfilesError


class Property(CxxPointer):
    '''
    A :py:class:`Property` holds the data used in properties in
    :py:class:`Frame` and :py:class:`Atom`. A property can have various types:
    bool, double, string or 3D vectors.

    This class is not meant for direct use, but is an internal class.
    '''

    def __init__(self, value):
        '''Create a new property containing the given value'''
        if isinstance(value, bool):
            ptr = self.ffi.chfl_property_bool(c_bool(value))
        elif isinstance(value, (float, int)):
            ptr = self.ffi.chfl_property_double(c_double(value))
        elif _is_string(value):
            ptr = self.ffi.chfl_property_string(value.encode("utf8"))
        elif _is_vector3d(value):
            value = chfl_vector3d(value[0], value[1], value[2])
            ptr = self.ffi.chfl_property_vector3d(value)
        else:
            raise ChemfilesError(
                "can not create a Property with this value"
            )

        super(Property, self).__init__(ptr)

    def __del__(self):
        if hasattr(self, 'ptr'):
            self.ffi.chfl_property_free(self)

    def get(self):
        kind = chfl_property_kind()
        self.ffi.chfl_property_get_kind(self, kind)
        if kind.value == chfl_property_kind.CHFL_PROPERTY_BOOL:
            value = c_bool()
            self.ffi.chfl_property_get_bool(self, value)
            return value.value
        if kind.value == chfl_property_kind.CHFL_PROPERTY_DOUBLE:
            value = c_double()
            self.ffi.chfl_property_get_double(self, value)
            return value.value
        if kind.value == chfl_property_kind.CHFL_PROPERTY_STRING:
            def callback(buffer, size):
                self.ffi.chfl_property_get_string(self, buffer, size)
            return _call_with_growing_buffer(callback, initial=32)
        if kind.value == chfl_property_kind.CHFL_PROPERTY_VECTOR3D:
            value = chfl_vector3d()
            self.ffi.chfl_property_get_vector3d(self, value)
            return value[0], value[1], value[2]
        else:
            raise ChemfilesError("unknown property kind, this is a bug")


def _is_string(value):
    if sys.version_info[0] == 3:
        return isinstance(value, str)
    else:
        return isinstance(value, basestring)


def _is_vector3d(value):
    try:
        a = np.array(value, dtype="double")
        return len(a) >= 3
    except:
        return False
