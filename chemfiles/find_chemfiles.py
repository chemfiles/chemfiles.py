# -* coding: utf-8 -*
import os
from ctypes import cdll


def load_clib():
    libname = os.path.join(os.path.dirname(__file__), "_chemfiles.so")
    try:
        return cdll.LoadLibrary(libname)
    except OSError:
        # We could not find chemfiles ...
        raise ImportError("Could not find the chemfiles library. " +
                          "Are you sure it is installed?")
