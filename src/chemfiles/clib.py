# -* coding: utf-8 -*
import os
import sys
import struct
from ctypes import cdll, c_double, POINTER
from ctypes import sizeof, c_voidp

from .location import CHEMFILES_LOCATION, __file__ as location_file_path


class FindChemfilesLibrary(object):
    def __init__(self):
        self._cache = None

    def __call__(self):
        if self._cache is None:
            check_dll(CHEMFILES_LOCATION)
            try:
                self._cache = cdll.LoadLibrary(CHEMFILES_LOCATION)
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


def check_dll(path):
    if not sys.platform.startswith("win"):
        return
    if not os.path.isfile(path):
        return

    import struct

    IMAGE_FILE_MACHINE_I386 = 332
    IMAGE_FILE_MACHINE_AMD64 = 34404

    machine = None
    with open(path, 'rb') as fd:
        header = fd.read(2).decode(encoding="utf-8", errors="strict")
        if header != "MZ":
            raise ImportError(path + " is not a DLL")
        else:
            fd.seek(60)
            header = fd.read(4)
            header_offset = struct.unpack("<L", header)[0]
            fd.seek(header_offset + 4)
            header = fd.read(2)
            machine = struct.unpack("<H", header)[0]

    if sizeof(c_voidp) == 4 and machine != IMAGE_FILE_MACHINE_I386:
        raise ImportError("Python is 32-bit, but chemfiles.dll is not")
    elif sizeof(c_voidp) == 8 and machine != IMAGE_FILE_MACHINE_AMD64:
        raise ImportError("Python is 64-bit, but chemfiles.dll is not")


_get_c_library = FindChemfilesLibrary()
