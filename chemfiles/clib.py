# -* coding: utf-8 -*
import os
import sys
from ctypes import cdll, c_double, POINTER
from ctypes import sizeof, c_voidp


class FindChemfilesLibrary(object):
    def __init__(self):
        self._cache = None

    def __call__(self):
        if self._cache is None:
            path = _lib_path()
            self._cache = cdll.LoadLibrary(path)

            from .ffi import set_interface
            from .ffi import CHFL_FRAME, CHFL_ATOM, chfl_vector3d
            set_interface(self._cache)
            # We update the arguments here, as ctypes can not pass a NULL value
            # as the last parameter
            self._cache.chfl_frame_add_atom.argtypes = [
                POINTER(CHFL_FRAME), POINTER(CHFL_ATOM),
                chfl_vector3d, POINTER(c_double)
            ]

            from .utils import _set_default_warning_callback
            _set_default_warning_callback()
        return self._cache


def _lib_path():
    root = os.path.dirname(__file__)
    if sys.platform.startswith("darwin"):
        return os.path.join(root, "lib", "libchemfiles.dylib")
    elif sys.platform.startswith("linux"):
        return os.path.join(root, "lib", "libchemfiles.so")
    elif sys.platform.startswith("win"):
        candidates = [
            os.path.join(root, "bin", "libchemfiles.dll"),  # MinGW
            os.path.join(root, "bin", "chemfiles.dll"),     # MSVC
        ]
        for path in candidates:
            if os.path.isfile(path):
                _check_dll(path)
                return path
        raise ImportError("Could not find chemfiles DLL")
    else:
        raise ImportError("Unknown platform. Please edit this file")


def _check_dll(path):
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
