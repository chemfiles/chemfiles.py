# -* coding: utf-8 -*
import sys
import os
from ctypes import cdll


def load_clib():
    libname = os.path.join(os.path.dirname(__file__), "libchemharp.")
    libname += dl_ext()
    try:
        return cdll.LoadLibrary(libname)
    except OSError:
        # We could not find chemharp ...
        raise ImportError("Could not find the Chemharp library. " +
                          "Are you sure it is installed?")


def dl_ext():
    if sys.platform.startswith("win32"):
        return "dll"
    elif sys.platform.startswith("linux"):
        return "so"
    elif sys.platform.startswith("darwin"):
        return "dylib"
