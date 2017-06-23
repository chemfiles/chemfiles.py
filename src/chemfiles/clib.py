# -* coding: utf-8 -*
import os
import sys
from ctypes import cdll, c_double, POINTER

from .location import CHEMFILES_LOCATION, __file__ as location_file_path


class FindChemfilesLibrary(object):
    def __init__(self):
        self._cache = None

    def __call__(self):
        if self._cache is None:
            try:
                self._cache = cdll.LoadLibrary(lib_path(CHEMFILES_LOCATION))
            except OSError:
                if location_file_path.endswith(".pyc"):
                    path = location_file_path[:-1]
                else:
                    path = location_file_path
                raise ImportError(
                    "Could not find chemfiles c++ library. " +
                    "Please check the path defined in " + path
                )

            from .ffi import set_interface
            from .ffi import CHFL_FRAME, CHFL_ATOM, chfl_vector_t
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


_get_c_library = FindChemfilesLibrary()
