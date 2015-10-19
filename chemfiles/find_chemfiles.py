# -* coding: utf-8 -*
import os
from ctypes import cdll
from ctypes.util import find_library


def load_clib():
    libpath = find_library("chemfiles")
    if not libpath:
        # Rely on the library built by the setup.py function
        libpath = os.path.join(os.path.dirname(__file__), "_chemfiles.so")
    try:
        return cdll.LoadLibrary(libpath)
    except OSError:
        # We could not find chemfiles ...
        raise ImportError("Could not find the chemfiles library. " +
                          "Are you sure it is installed?")
