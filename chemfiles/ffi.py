# -* coding: utf-8 -*
# Chemfiles, an efficient IO library for chemistry file formats
# Copyright (C) 2015 Guillaume Fraux
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/
#
# =========================================================================== #
# !!!! AUTO-GENERATED FILE !!!! Do not edit. See the bindgen repository for
# the generation code (https://github.com/chemfiles/bindgen).
# This file contains Python ctype interface to the C API
# =========================================================================== #

'''
Foreign function interface declaration for the Python interface to chemfiles
'''

import sys

from numpy.ctypeslib import ndpointer
import numpy as np
from ctypes import *

from .errors import _check
from .find_chemfiles import load_clib


class ChemfilesLibrary(object):
    def __init__(self):
        self._cache = None

    def __call__(self):
        if self._cache is None:
            self._cache = load_clib()
            set_interface(self._cache)
        return self._cache

get_c_library = ChemfilesLibrary()


class CHFL_LOG_LEVEL(c_int):
    CHFL_LOG_NONE = 0
    CHFL_LOG_ERROR = 1
    CHFL_LOG_WARNING = 2
    CHFL_LOG_INFO = 3
    CHFL_LOG_DEBUG = 4


class CHFL_CELL_TYPES(c_int):
    CHFL_CELL_ORTHOROMBIC = 0
    CHFL_CELL_TRICLINIC = 1
    CHFL_CELL_INFINITE = 2


class CHFL_ATOM_TYPES(c_int):
    CHFL_ATOM_ELEMENT = 0
    CHFL_ATOM_CORSE_GRAIN = 1
    CHFL_ATOM_DUMMY = 2
    CHFL_ATOM_UNDEFINED = 3


class CHFL_TRAJECTORY(Structure):
    pass


class CHFL_CELL(Structure):
    pass


class CHFL_ATOM(Structure):
    pass


class CHFL_FRAME(Structure):
    pass


class CHFL_TOPOLOGY(Structure):
    pass


def set_interface(c_lib):
    # Function "chfl_strerror", at chemfiles.h:59
    c_lib.chfl_strerror.argtypes = [c_int]
    c_lib.chfl_strerror.restype = c_char_p
    

    # Function "chfl_last_error", at chemfiles.h:65
    c_lib.chfl_last_error.argtypes = []
    c_lib.chfl_last_error.restype = c_char_p
    

    # Function "chfl_loglevel", at chemfiles.h:86
    c_lib.chfl_loglevel.argtypes = [POINTER(c_int)]
    c_lib.chfl_loglevel.restype = c_int
    c_lib.chfl_loglevel.errcheck = _check

    # Function "chfl_set_loglevel", at chemfiles.h:93
    c_lib.chfl_set_loglevel.argtypes = [c_int]
    c_lib.chfl_set_loglevel.restype = c_int
    c_lib.chfl_set_loglevel.errcheck = _check

    # Function "chfl_logfile", at chemfiles.h:100
    c_lib.chfl_logfile.argtypes = [c_char_p]
    c_lib.chfl_logfile.restype = c_int
    c_lib.chfl_logfile.errcheck = _check

    # Function "chfl_log_stderr", at chemfiles.h:106
    c_lib.chfl_log_stderr.argtypes = []
    c_lib.chfl_log_stderr.restype = c_int
    c_lib.chfl_log_stderr.errcheck = _check

    # Function "chfl_trajectory_open", at chemfiles.h:115
    c_lib.chfl_trajectory_open.argtypes = [c_char_p, c_char_p]
    c_lib.chfl_trajectory_open.restype = POINTER(CHFL_TRAJECTORY)
    

    # Function "chfl_trajectory_with_format", at chemfiles.h:124
    c_lib.chfl_trajectory_with_format.argtypes = [c_char_p, c_char_p, c_char_p]
    c_lib.chfl_trajectory_with_format.restype = POINTER(CHFL_TRAJECTORY)
    

    # Function "chfl_trajectory_read", at chemfiles.h:132
    c_lib.chfl_trajectory_read.argtypes = [POINTER(CHFL_TRAJECTORY), POINTER(CHFL_FRAME)]
    c_lib.chfl_trajectory_read.restype = c_int
    c_lib.chfl_trajectory_read.errcheck = _check

    # Function "chfl_trajectory_read_step", at chemfiles.h:141
    c_lib.chfl_trajectory_read_step.argtypes = [POINTER(CHFL_TRAJECTORY), c_size_t, POINTER(CHFL_FRAME)]
    c_lib.chfl_trajectory_read_step.restype = c_int
    c_lib.chfl_trajectory_read_step.errcheck = _check

    # Function "chfl_trajectory_write", at chemfiles.h:149
    c_lib.chfl_trajectory_write.argtypes = [POINTER(CHFL_TRAJECTORY), POINTER(CHFL_FRAME)]
    c_lib.chfl_trajectory_write.restype = c_int
    c_lib.chfl_trajectory_write.errcheck = _check

    # Function "chfl_trajectory_set_topology", at chemfiles.h:159
    c_lib.chfl_trajectory_set_topology.argtypes = [POINTER(CHFL_TRAJECTORY), POINTER(CHFL_TOPOLOGY)]
    c_lib.chfl_trajectory_set_topology.restype = c_int
    c_lib.chfl_trajectory_set_topology.errcheck = _check

    # Function "chfl_trajectory_set_topology_file", at chemfiles.h:168
    c_lib.chfl_trajectory_set_topology_file.argtypes = [POINTER(CHFL_TRAJECTORY), c_char_p]
    c_lib.chfl_trajectory_set_topology_file.restype = c_int
    c_lib.chfl_trajectory_set_topology_file.errcheck = _check

    # Function "chfl_trajectory_set_cell", at chemfiles.h:178
    c_lib.chfl_trajectory_set_cell.argtypes = [POINTER(CHFL_TRAJECTORY), POINTER(CHFL_CELL)]
    c_lib.chfl_trajectory_set_cell.restype = c_int
    c_lib.chfl_trajectory_set_cell.errcheck = _check

    # Function "chfl_trajectory_nsteps", at chemfiles.h:186
    c_lib.chfl_trajectory_nsteps.argtypes = [POINTER(CHFL_TRAJECTORY), POINTER(c_size_t)]
    c_lib.chfl_trajectory_nsteps.restype = c_int
    c_lib.chfl_trajectory_nsteps.errcheck = _check

    # Function "chfl_trajectory_sync", at chemfiles.h:193
    c_lib.chfl_trajectory_sync.argtypes = [POINTER(CHFL_TRAJECTORY)]
    c_lib.chfl_trajectory_sync.restype = c_int
    c_lib.chfl_trajectory_sync.errcheck = _check

    # Function "chfl_trajectory_close", at chemfiles.h:200
    c_lib.chfl_trajectory_close.argtypes = [POINTER(CHFL_TRAJECTORY)]
    c_lib.chfl_trajectory_close.restype = c_int
    c_lib.chfl_trajectory_close.errcheck = _check

    # Function "chfl_frame", at chemfiles.h:209
    c_lib.chfl_frame.argtypes = [c_size_t]
    c_lib.chfl_frame.restype = POINTER(CHFL_FRAME)
    

    # Function "chfl_frame_atoms_count", at chemfiles.h:217
    c_lib.chfl_frame_atoms_count.argtypes = [POINTER(CHFL_FRAME), POINTER(c_size_t)]
    c_lib.chfl_frame_atoms_count.restype = c_int
    c_lib.chfl_frame_atoms_count.errcheck = _check

    # Function "chfl_frame_positions", at chemfiles.h:226
    c_lib.chfl_frame_positions.argtypes = [POINTER(CHFL_FRAME), ndpointer(np.float32, flags="C_CONTIGUOUS", ndim=2), c_size_t]
    c_lib.chfl_frame_positions.restype = c_int
    c_lib.chfl_frame_positions.errcheck = _check

    # Function "chfl_frame_set_positions", at chemfiles.h:235
    c_lib.chfl_frame_set_positions.argtypes = [POINTER(CHFL_FRAME), ndpointer(np.float32, flags="C_CONTIGUOUS", ndim=2), c_size_t]
    c_lib.chfl_frame_set_positions.restype = c_int
    c_lib.chfl_frame_set_positions.errcheck = _check

    # Function "chfl_frame_velocities", at chemfiles.h:244
    c_lib.chfl_frame_velocities.argtypes = [POINTER(CHFL_FRAME), ndpointer(np.float32, flags="C_CONTIGUOUS", ndim=2), c_size_t]
    c_lib.chfl_frame_velocities.restype = c_int
    c_lib.chfl_frame_velocities.errcheck = _check

    # Function "chfl_frame_set_velocities", at chemfiles.h:253
    c_lib.chfl_frame_set_velocities.argtypes = [POINTER(CHFL_FRAME), ndpointer(np.float32, flags="C_CONTIGUOUS", ndim=2), c_size_t]
    c_lib.chfl_frame_set_velocities.restype = c_int
    c_lib.chfl_frame_set_velocities.errcheck = _check

    # Function "chfl_frame_has_velocities", at chemfiles.h:261
    c_lib.chfl_frame_has_velocities.argtypes = [POINTER(CHFL_FRAME), POINTER(c_bool)]
    c_lib.chfl_frame_has_velocities.restype = c_int
    c_lib.chfl_frame_has_velocities.errcheck = _check

    # Function "chfl_frame_set_cell", at chemfiles.h:269
    c_lib.chfl_frame_set_cell.argtypes = [POINTER(CHFL_FRAME), POINTER(CHFL_CELL)]
    c_lib.chfl_frame_set_cell.restype = c_int
    c_lib.chfl_frame_set_cell.errcheck = _check

    # Function "chfl_frame_set_topology", at chemfiles.h:277
    c_lib.chfl_frame_set_topology.argtypes = [POINTER(CHFL_FRAME), POINTER(CHFL_TOPOLOGY)]
    c_lib.chfl_frame_set_topology.restype = c_int
    c_lib.chfl_frame_set_topology.errcheck = _check

    # Function "chfl_frame_step", at chemfiles.h:285
    c_lib.chfl_frame_step.argtypes = [POINTER(CHFL_FRAME), POINTER(c_size_t)]
    c_lib.chfl_frame_step.restype = c_int
    c_lib.chfl_frame_step.errcheck = _check

    # Function "chfl_frame_set_step", at chemfiles.h:293
    c_lib.chfl_frame_set_step.argtypes = [POINTER(CHFL_FRAME), c_size_t]
    c_lib.chfl_frame_set_step.restype = c_int
    c_lib.chfl_frame_set_step.errcheck = _check

    # Function "chfl_frame_guess_topology", at chemfiles.h:303
    c_lib.chfl_frame_guess_topology.argtypes = [POINTER(CHFL_FRAME), c_bool]
    c_lib.chfl_frame_guess_topology.restype = c_int
    c_lib.chfl_frame_guess_topology.errcheck = _check

    # Function "chfl_frame_free", at chemfiles.h:310
    c_lib.chfl_frame_free.argtypes = [POINTER(CHFL_FRAME)]
    c_lib.chfl_frame_free.restype = c_int
    c_lib.chfl_frame_free.errcheck = _check

    # Function "chfl_cell", at chemfiles.h:318
    c_lib.chfl_cell.argtypes = [c_double, c_double, c_double]
    c_lib.chfl_cell.restype = POINTER(CHFL_CELL)
    

    # Function "chfl_cell_triclinic", at chemfiles.h:326
    c_lib.chfl_cell_triclinic.argtypes = [c_double, c_double, c_double, c_double, c_double, c_double]
    c_lib.chfl_cell_triclinic.restype = POINTER(CHFL_CELL)
    

    # Function "chfl_cell_from_frame", at chemfiles.h:333
    c_lib.chfl_cell_from_frame.argtypes = [POINTER(CHFL_FRAME)]
    c_lib.chfl_cell_from_frame.restype = POINTER(CHFL_CELL)
    

    # Function "chfl_cell_volume", at chemfiles.h:341
    c_lib.chfl_cell_volume.argtypes = [POINTER(CHFL_CELL), POINTER(c_double)]
    c_lib.chfl_cell_volume.restype = c_int
    c_lib.chfl_cell_volume.errcheck = _check

    # Function "chfl_cell_lengths", at chemfiles.h:349
    c_lib.chfl_cell_lengths.argtypes = [POINTER(CHFL_CELL), POINTER(c_double), POINTER(c_double), POINTER(c_double)]
    c_lib.chfl_cell_lengths.restype = c_int
    c_lib.chfl_cell_lengths.errcheck = _check

    # Function "chfl_cell_set_lengths", at chemfiles.h:357
    c_lib.chfl_cell_set_lengths.argtypes = [POINTER(CHFL_CELL), c_double, c_double, c_double]
    c_lib.chfl_cell_set_lengths.restype = c_int
    c_lib.chfl_cell_set_lengths.errcheck = _check

    # Function "chfl_cell_angles", at chemfiles.h:365
    c_lib.chfl_cell_angles.argtypes = [POINTER(CHFL_CELL), POINTER(c_double), POINTER(c_double), POINTER(c_double)]
    c_lib.chfl_cell_angles.restype = c_int
    c_lib.chfl_cell_angles.errcheck = _check

    # Function "chfl_cell_set_angles", at chemfiles.h:373
    c_lib.chfl_cell_set_angles.argtypes = [POINTER(CHFL_CELL), c_double, c_double, c_double]
    c_lib.chfl_cell_set_angles.restype = c_int
    c_lib.chfl_cell_set_angles.errcheck = _check

    # Function "chfl_cell_matrix", at chemfiles.h:381
    c_lib.chfl_cell_matrix.argtypes = [POINTER(CHFL_CELL), ndpointer(np.float64, flags="C_CONTIGUOUS", ndim=2, shape=(3, 3))]
    c_lib.chfl_cell_matrix.restype = c_int
    c_lib.chfl_cell_matrix.errcheck = _check

    # Function "chfl_cell_type", at chemfiles.h:399
    c_lib.chfl_cell_type.argtypes = [POINTER(CHFL_CELL), POINTER(c_int)]
    c_lib.chfl_cell_type.restype = c_int
    c_lib.chfl_cell_type.errcheck = _check

    # Function "chfl_cell_set_type", at chemfiles.h:407
    c_lib.chfl_cell_set_type.argtypes = [POINTER(CHFL_CELL), c_int]
    c_lib.chfl_cell_set_type.restype = c_int
    c_lib.chfl_cell_set_type.errcheck = _check

    # Function "chfl_cell_periodicity", at chemfiles.h:415
    c_lib.chfl_cell_periodicity.argtypes = [POINTER(CHFL_CELL), POINTER(c_bool), POINTER(c_bool), POINTER(c_bool)]
    c_lib.chfl_cell_periodicity.restype = c_int
    c_lib.chfl_cell_periodicity.errcheck = _check

    # Function "chfl_cell_set_periodicity", at chemfiles.h:423
    c_lib.chfl_cell_set_periodicity.argtypes = [POINTER(CHFL_CELL), c_bool, c_bool, c_bool]
    c_lib.chfl_cell_set_periodicity.restype = c_int
    c_lib.chfl_cell_set_periodicity.errcheck = _check

    # Function "chfl_cell_free", at chemfiles.h:430
    c_lib.chfl_cell_free.argtypes = [POINTER(CHFL_CELL)]
    c_lib.chfl_cell_free.restype = c_int
    c_lib.chfl_cell_free.errcheck = _check

    # Function "chfl_topology", at chemfiles.h:438
    c_lib.chfl_topology.argtypes = []
    c_lib.chfl_topology.restype = POINTER(CHFL_TOPOLOGY)
    

    # Function "chfl_topology_from_frame", at chemfiles.h:445
    c_lib.chfl_topology_from_frame.argtypes = [POINTER(CHFL_FRAME)]
    c_lib.chfl_topology_from_frame.restype = POINTER(CHFL_TOPOLOGY)
    

    # Function "chfl_topology_atoms_count", at chemfiles.h:453
    c_lib.chfl_topology_atoms_count.argtypes = [POINTER(CHFL_TOPOLOGY), POINTER(c_size_t)]
    c_lib.chfl_topology_atoms_count.restype = c_int
    c_lib.chfl_topology_atoms_count.errcheck = _check

    # Function "chfl_topology_append", at chemfiles.h:461
    c_lib.chfl_topology_append.argtypes = [POINTER(CHFL_TOPOLOGY), POINTER(CHFL_ATOM)]
    c_lib.chfl_topology_append.restype = c_int
    c_lib.chfl_topology_append.errcheck = _check

    # Function "chfl_topology_remove", at chemfiles.h:469
    c_lib.chfl_topology_remove.argtypes = [POINTER(CHFL_TOPOLOGY), c_size_t]
    c_lib.chfl_topology_remove.restype = c_int
    c_lib.chfl_topology_remove.errcheck = _check

    # Function "chfl_topology_isbond", at chemfiles.h:478
    c_lib.chfl_topology_isbond.argtypes = [POINTER(CHFL_TOPOLOGY), c_size_t, c_size_t, POINTER(c_bool)]
    c_lib.chfl_topology_isbond.restype = c_int
    c_lib.chfl_topology_isbond.errcheck = _check

    # Function "chfl_topology_isangle", at chemfiles.h:487
    c_lib.chfl_topology_isangle.argtypes = [POINTER(CHFL_TOPOLOGY), c_size_t, c_size_t, c_size_t, POINTER(c_bool)]
    c_lib.chfl_topology_isangle.restype = c_int
    c_lib.chfl_topology_isangle.errcheck = _check

    # Function "chfl_topology_isdihedral", at chemfiles.h:496
    c_lib.chfl_topology_isdihedral.argtypes = [POINTER(CHFL_TOPOLOGY), c_size_t, c_size_t, c_size_t, c_size_t, POINTER(c_bool)]
    c_lib.chfl_topology_isdihedral.restype = c_int
    c_lib.chfl_topology_isdihedral.errcheck = _check

    # Function "chfl_topology_bonds_count", at chemfiles.h:504
    c_lib.chfl_topology_bonds_count.argtypes = [POINTER(CHFL_TOPOLOGY), POINTER(c_size_t)]
    c_lib.chfl_topology_bonds_count.restype = c_int
    c_lib.chfl_topology_bonds_count.errcheck = _check

    # Function "chfl_topology_angles_count", at chemfiles.h:512
    c_lib.chfl_topology_angles_count.argtypes = [POINTER(CHFL_TOPOLOGY), POINTER(c_size_t)]
    c_lib.chfl_topology_angles_count.restype = c_int
    c_lib.chfl_topology_angles_count.errcheck = _check

    # Function "chfl_topology_dihedrals_count", at chemfiles.h:520
    c_lib.chfl_topology_dihedrals_count.argtypes = [POINTER(CHFL_TOPOLOGY), POINTER(c_size_t)]
    c_lib.chfl_topology_dihedrals_count.restype = c_int
    c_lib.chfl_topology_dihedrals_count.errcheck = _check

    # Function "chfl_topology_bonds", at chemfiles.h:530
    c_lib.chfl_topology_bonds.argtypes = [POINTER(CHFL_TOPOLOGY), ndpointer(np.uintp, flags="C_CONTIGUOUS", ndim=2), c_size_t]
    c_lib.chfl_topology_bonds.restype = c_int
    c_lib.chfl_topology_bonds.errcheck = _check

    # Function "chfl_topology_angles", at chemfiles.h:540
    c_lib.chfl_topology_angles.argtypes = [POINTER(CHFL_TOPOLOGY), ndpointer(np.uintp, flags="C_CONTIGUOUS", ndim=2), c_size_t]
    c_lib.chfl_topology_angles.restype = c_int
    c_lib.chfl_topology_angles.errcheck = _check

    # Function "chfl_topology_dihedrals", at chemfiles.h:550
    c_lib.chfl_topology_dihedrals.argtypes = [POINTER(CHFL_TOPOLOGY), ndpointer(np.uintp, flags="C_CONTIGUOUS", ndim=2), c_size_t]
    c_lib.chfl_topology_dihedrals.restype = c_int
    c_lib.chfl_topology_dihedrals.errcheck = _check

    # Function "chfl_topology_add_bond", at chemfiles.h:558
    c_lib.chfl_topology_add_bond.argtypes = [POINTER(CHFL_TOPOLOGY), c_size_t, c_size_t]
    c_lib.chfl_topology_add_bond.restype = c_int
    c_lib.chfl_topology_add_bond.errcheck = _check

    # Function "chfl_topology_remove_bond", at chemfiles.h:566
    c_lib.chfl_topology_remove_bond.argtypes = [POINTER(CHFL_TOPOLOGY), c_size_t, c_size_t]
    c_lib.chfl_topology_remove_bond.restype = c_int
    c_lib.chfl_topology_remove_bond.errcheck = _check

    # Function "chfl_topology_free", at chemfiles.h:573
    c_lib.chfl_topology_free.argtypes = [POINTER(CHFL_TOPOLOGY)]
    c_lib.chfl_topology_free.restype = c_int
    c_lib.chfl_topology_free.errcheck = _check

    # Function "chfl_atom", at chemfiles.h:582
    c_lib.chfl_atom.argtypes = [c_char_p]
    c_lib.chfl_atom.restype = POINTER(CHFL_ATOM)
    

    # Function "chfl_atom_from_frame", at chemfiles.h:590
    c_lib.chfl_atom_from_frame.argtypes = [POINTER(CHFL_FRAME), c_size_t]
    c_lib.chfl_atom_from_frame.restype = POINTER(CHFL_ATOM)
    

    # Function "chfl_atom_from_topology", at chemfiles.h:598
    c_lib.chfl_atom_from_topology.argtypes = [POINTER(CHFL_TOPOLOGY), c_size_t]
    c_lib.chfl_atom_from_topology.restype = POINTER(CHFL_ATOM)
    

    # Function "chfl_atom_mass", at chemfiles.h:606
    c_lib.chfl_atom_mass.argtypes = [POINTER(CHFL_ATOM), POINTER(c_float)]
    c_lib.chfl_atom_mass.restype = c_int
    c_lib.chfl_atom_mass.errcheck = _check

    # Function "chfl_atom_set_mass", at chemfiles.h:614
    c_lib.chfl_atom_set_mass.argtypes = [POINTER(CHFL_ATOM), c_float]
    c_lib.chfl_atom_set_mass.restype = c_int
    c_lib.chfl_atom_set_mass.errcheck = _check

    # Function "chfl_atom_charge", at chemfiles.h:622
    c_lib.chfl_atom_charge.argtypes = [POINTER(CHFL_ATOM), POINTER(c_float)]
    c_lib.chfl_atom_charge.restype = c_int
    c_lib.chfl_atom_charge.errcheck = _check

    # Function "chfl_atom_set_charge", at chemfiles.h:630
    c_lib.chfl_atom_set_charge.argtypes = [POINTER(CHFL_ATOM), c_float]
    c_lib.chfl_atom_set_charge.restype = c_int
    c_lib.chfl_atom_set_charge.errcheck = _check

    # Function "chfl_atom_name", at chemfiles.h:639
    c_lib.chfl_atom_name.argtypes = [POINTER(CHFL_ATOM), c_char_p, c_size_t]
    c_lib.chfl_atom_name.restype = c_int
    c_lib.chfl_atom_name.errcheck = _check

    # Function "chfl_atom_set_name", at chemfiles.h:647
    c_lib.chfl_atom_set_name.argtypes = [POINTER(CHFL_ATOM), c_char_p]
    c_lib.chfl_atom_set_name.restype = c_int
    c_lib.chfl_atom_set_name.errcheck = _check

    # Function "chfl_atom_full_name", at chemfiles.h:656
    c_lib.chfl_atom_full_name.argtypes = [POINTER(CHFL_ATOM), c_char_p, c_size_t]
    c_lib.chfl_atom_full_name.restype = c_int
    c_lib.chfl_atom_full_name.errcheck = _check

    # Function "chfl_atom_vdw_radius", at chemfiles.h:664
    c_lib.chfl_atom_vdw_radius.argtypes = [POINTER(CHFL_ATOM), POINTER(c_double)]
    c_lib.chfl_atom_vdw_radius.restype = c_int
    c_lib.chfl_atom_vdw_radius.errcheck = _check

    # Function "chfl_atom_covalent_radius", at chemfiles.h:672
    c_lib.chfl_atom_covalent_radius.argtypes = [POINTER(CHFL_ATOM), POINTER(c_double)]
    c_lib.chfl_atom_covalent_radius.restype = c_int
    c_lib.chfl_atom_covalent_radius.errcheck = _check

    # Function "chfl_atom_atomic_number", at chemfiles.h:680
    c_lib.chfl_atom_atomic_number.argtypes = [POINTER(CHFL_ATOM), POINTER(c_int)]
    c_lib.chfl_atom_atomic_number.restype = c_int
    c_lib.chfl_atom_atomic_number.errcheck = _check

    # Function "chfl_atom_type", at chemfiles.h:701
    c_lib.chfl_atom_type.argtypes = [POINTER(CHFL_ATOM), POINTER(c_int)]
    c_lib.chfl_atom_type.restype = c_int
    c_lib.chfl_atom_type.errcheck = _check

    # Function "chfl_atom_set_type", at chemfiles.h:709
    c_lib.chfl_atom_set_type.argtypes = [POINTER(CHFL_ATOM), c_int]
    c_lib.chfl_atom_set_type.restype = c_int
    c_lib.chfl_atom_set_type.errcheck = _check

    # Function "chfl_atom_free", at chemfiles.h:716
    c_lib.chfl_atom_free.argtypes = [POINTER(CHFL_ATOM)]
    c_lib.chfl_atom_free.restype = c_int
    c_lib.chfl_atom_free.errcheck = _check
