# -* coding: utf-8 -*
import sys
import os
from ctypes import cdll


def load_clib():
    libname = os.path.join(os.path.dirname(__file__), "libchemfiles.")
    libname += dl_ext()
    try:
        return cdll.LoadLibrary(libname)
    except OSError:
        # We could not find chemfiles ...
        raise ImportError("Could not find the chemfiles library. " +
                          "Are you sure it is installed?")


def dl_ext():
    if sys.platform.startswith("win32"):
        return "dll"
    elif sys.platform.startswith("linux"):
        return "so"
    elif sys.platform.startswith("darwin"):
        return "dylib"
