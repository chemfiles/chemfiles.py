# -* coding: utf-8 -*
import sys
import os
from ctypes import cdll
from ctypes.util import find_library


def find_chemharp():
    libpath = find_library("chemharp")
    if libpath:
        # chemharp was found in system path
        return cdll.LoadLibrary(libpath)

    libname = "libchemharp." + dl_ext()

    # Try looking in PYTHONPATH
    for path in sys.path:
        libpath = os.path.join(path, libname)
        if os.path.isfile(libpath):
            return cdll.LoadLibrary(libpath)

    # We could not find chemharp ...
    raise ImportError(
        "Could not find the Chemharp library. Are you sure it is installed?"
    )


def dl_ext():
    if sys.platform.startswith("win32"):
        return "dll"
    elif sys.platform.startswith("linux"):
        return "so"
    elif sys.platform.startswith("darwin"):
        return "dylib"
