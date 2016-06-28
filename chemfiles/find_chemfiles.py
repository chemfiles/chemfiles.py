# -* coding: utf-8 -*
import os
from ctypes import cdll
from ctypes.util import find_library

from chemfiles import ffi

ROOT = os.path.dirname(__file__)


def load_clib():
    '''Load chemfiles C++ library'''
    libpath = find_library("chemfiles")
    if not libpath:
        # Rely on the library built by the setup.py function
        libpath = os.path.join(ROOT, "_chemfiles.so")
    try:
        return cdll.LoadLibrary(libpath)
    except OSError:
        raise ImportError(
            "Could not find chemfiles library. Are you sure it's installed?"
        )


class ChemfilesLibrary(object):
    def __init__(self):
        self._cache = None

    def __call__(self):
        if self._cache is None:
            self._cache = load_clib()
            ffi.set_interface(self._cache)
        return self._cache
