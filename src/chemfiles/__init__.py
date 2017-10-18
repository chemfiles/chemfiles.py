# -*- coding=utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from .utils import ChemfilesError, set_warnings_callback, add_configuration
from .atom import Atom
from .residue import Residue
from .topology import Topology
from .cell import UnitCell, CellShape
from .frame import Frame
from .trajectory import Trajectory
from .selection import Selection
from .property import Property

# Setup work
from .utils import _set_default_warning_callback
from .clib import _get_c_library
_set_default_warning_callback()

__version__ = _get_c_library().chfl_version().decode("utf8")
assert(__version__.startswith("0.8"))
