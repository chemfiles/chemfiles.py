# -* coding: utf-8 -*
import os
import sys
from ctypes import cdll, CDLL, c_double, POINTER
from typing import Optional

try:
    from .external import EXTERNAL_CHEMFILES
except ImportError:
    EXTERNAL_CHEMFILES = ""


class FindChemfilesLibrary(object):
    def __init__(self):
        # type: () -> None

        self._cache = None  # type: Optional[CDLL]

    def __call__(self):
        # type: () -> CDLL
        if self._cache is None:
            path = _lib_path()
            self._cache = cdll.LoadLibrary(path)

            from .ffi import set_interface
            from .ffi import CHFL_FRAME, CHFL_ATOM, chfl_vector3d

            set_interface(self._cache)
            # We update the arguments here, as ctypes can not pass a NULL value
            # as the last parameter
            self._cache.chfl_frame_add_atom.argtypes = [
                POINTER(CHFL_FRAME),
                POINTER(CHFL_ATOM),
                chfl_vector3d,
                POINTER(c_double),
            ]

            from .misc import _set_default_warning_callback

            _set_default_warning_callback()
        return self._cache


def _lib_path():
    # type: () -> str
    if EXTERNAL_CHEMFILES:
        return EXTERNAL_CHEMFILES
    root = os.path.abspath(os.path.dirname(__file__))
    if sys.platform.startswith("darwin"):
        return os.path.join(root, "libchemfiles.dylib")
    elif sys.platform.startswith("linux"):
        return os.path.join(root, "libchemfiles.so")
    elif sys.platform.startswith("win"):
        candidates = [
            os.path.join(root, "libchemfiles.dll"),  # MinGW
            os.path.join(root, "chemfiles.dll"),  # MSVC
        ]
        for path in candidates:
            if os.path.isfile(path):
                _check_dll(path)
                return path
        raise ImportError("Could not find chemfiles DLL")
    else:
        raise ImportError("Unknown platform. Please edit this file")


def _check_dll(path):
    # type: (str) -> None
    import struct
    import platform

    IMAGE_FILE_MACHINE_I386 = 332
    IMAGE_FILE_MACHINE_AMD64 = 34404

    machine = None
    with open(path, "rb") as fd:
        header = fd.read(2)
        if header != b"MZ":
            raise ImportError(path + " is not a DLL")
        else:
            fd.seek(60)
            header = fd.read(4)
            header_offset = struct.unpack("<L", header)[0]
            fd.seek(header_offset + 4)
            header = fd.read(2)
            machine = struct.unpack("<H", header)[0]

    arch = platform.architecture()[0]
    if arch == "32bit":
        if machine != IMAGE_FILE_MACHINE_I386:
            raise ImportError("Python is 32-bit, but chemfiles.dll is not")
    elif arch == "64bit":
        if machine != IMAGE_FILE_MACHINE_AMD64:
            raise ImportError("Python is 64-bit, but chemfiles.dll is not")
    else:
        raise ImportError("Could not determine pointer size of Python")


_get_c_library = FindChemfilesLibrary()
