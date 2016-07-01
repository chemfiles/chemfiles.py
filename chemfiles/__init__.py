# -*- coding=utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from .find_chemfiles import ChemfilesLibrary

get_c_library = ChemfilesLibrary()
__version__ = get_c_library().chfl_version().decode("utf8")

from .errors import ChemfilesException, ArgumentError
from .atom import Atom, AtomType
from .topology import Topology
from .cell import UnitCell, CellType
from .frame import Frame
from .trajectory import Trajectory
from .selection import Selection
