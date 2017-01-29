# -*- coding=utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from .clib import FindChemfilesLibrary

get_c_library = FindChemfilesLibrary()
__version__ = get_c_library().chfl_version().decode("utf8")

from .errors import ChemfilesException, ArgumentError
from .atom import Atom
from .topology import Topology
from .cell import UnitCell, CellShape
from .frame import Frame
from .trajectory import Trajectory
from .selection import Selection
