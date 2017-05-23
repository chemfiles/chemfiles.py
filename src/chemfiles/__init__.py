# -*- coding=utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from .clib import FindChemfilesLibrary
get_c_library = FindChemfilesLibrary()

from .errors import ChemfilesException
from .atom import Atom
from .residue import Residue
from .topology import Topology
from .cell import UnitCell, CellShape
from .frame import Frame
from .trajectory import Trajectory
from .selection import Selection

from .errors import _set_default_warning_callback
_set_default_warning_callback()

__version__ = get_c_library().chfl_version().decode("utf8")
assert(__version__.startswith("0.7"))
