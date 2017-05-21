# -* coding: utf-8 -*
import os
import sys
from ctypes import cdll, c_double, POINTER

from chemfiles.ffi import set_interface, CHFL_FRAME, CHFL_ATOM, chfl_vector_t
from .location import CHEMFILES_LOCATION


class FindChemfilesLibrary(object):
    def __init__(self):
        self._cache = None

    def __call__(self):
        if self._cache is None:
            try:
                self._cache = cdll.LoadLibrary(lib_path(CHEMFILES_LOCATION))
            except OSError:
                raise ImportError("Could not find chemfiles library.")
            set_interface(self._cache)
            # We update the arguments here, as ctypes can not pass a NULL value
            # as the last parameter
            self._cache.chfl_frame_add_atom.argtypes = [
                POINTER(CHFL_FRAME), POINTER(CHFL_ATOM),
                chfl_vector_t, POINTER(c_double)
            ]
        return self._cache


def lib_path(location):
    """Library file name from the location"""
    if os.path.isfile(location):
        return location

    if sys.platform.startswith("win"):
        return location + ".dll"
    elif sys.platform.startswith("linux"):
        return "lib" + location + ".so"
    elif sys.platform.startswith("darwin"):
        return "lib" + location + ".dylib"
    else:
        raise OSError("Unknown os. Edit this file to add logic for your OS.")
