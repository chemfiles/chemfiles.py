# -* coding: utf-8 -*
# Chemharp, an efficient IO library for chemistry file formats
# Copyright (C) 2015 Guillaume Fraux
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/
#
# =========================================================================== #
# !!!! AUTO-GENERATED FILE !!!! Do not edit. See scripts/generate for the code.
# This file contains Python ctype interface to the C API
# =========================================================================== #

'''
Foreign function interface declaration for the Python interface to Chemharp
'''

import sys

from numpy.ctypeslib import ndpointer
import numpy as np

from ctypes import *

from .errors import _check
from .find_chemharp import find_chemharp

c_lib = find_chemharp()


class CHRP_LOG_LEVEL(c_int):
    CHRP_LOG_NONE = 0
    CHRP_LOG_ERROR = 1
    CHRP_LOG_WARNING = 2
    CHRP_LOG_INFO = 3
    CHRP_LOG_DEBUG = 4


class CHRP_CELL_TYPES(c_int):
    CHRP_CELL_ORTHOROMBIC = 0
    CHRP_CELL_TRICLINIC = 1
    CHRP_CELL_INFINITE = 2


class CHRP_TRAJECTORY(Structure):
    pass


class CHRP_CELL(Structure):
    pass


class CHRP_ATOM(Structure):
    pass


class CHRP_FRAME(Structure):
    pass


class CHRP_TOPOLOGY(Structure):
    pass

# Function "chrp_strerror", at chemharp.h:60
c_lib.chrp_strerror.argtypes = [c_int]
c_lib.chrp_strerror.restype = c_char_p


# Function "chrp_last_error", at chemharp.h:66
c_lib.chrp_last_error.argtypes = []
c_lib.chrp_last_error.restype = c_char_p


# Function "chrp_loglevel", at chemharp.h:87
c_lib.chrp_loglevel.argtypes = [POINTER(c_int)]
c_lib.chrp_loglevel.restype = c_int
c_lib.chrp_loglevel.errcheck = _check

# Function "chrp_set_loglevel", at chemharp.h:94
c_lib.chrp_set_loglevel.argtypes = [c_int]
c_lib.chrp_set_loglevel.restype = c_int
c_lib.chrp_set_loglevel.errcheck = _check

# Function "chrp_logfile", at chemharp.h:101
c_lib.chrp_logfile.argtypes = [c_char_p]
c_lib.chrp_logfile.restype = c_int
c_lib.chrp_logfile.errcheck = _check

# Function "chrp_log_stderr", at chemharp.h:107
c_lib.chrp_log_stderr.argtypes = []
c_lib.chrp_log_stderr.restype = c_int
c_lib.chrp_log_stderr.errcheck = _check

# Function "chrp_open", at chemharp.h:116
c_lib.chrp_open.argtypes = [c_char_p, c_char_p]
c_lib.chrp_open.restype = POINTER(CHRP_TRAJECTORY)


# Function "chrp_trajectory_read", at chemharp.h:124
c_lib.chrp_trajectory_read.argtypes = [POINTER(CHRP_TRAJECTORY), POINTER(CHRP_FRAME)]
c_lib.chrp_trajectory_read.restype = c_int
c_lib.chrp_trajectory_read.errcheck = _check

# Function "chrp_trajectory_read_step", at chemharp.h:133
c_lib.chrp_trajectory_read_step.argtypes = [POINTER(CHRP_TRAJECTORY), c_size_t, POINTER(CHRP_FRAME)]
c_lib.chrp_trajectory_read_step.restype = c_int
c_lib.chrp_trajectory_read_step.errcheck = _check

# Function "chrp_trajectory_write", at chemharp.h:141
c_lib.chrp_trajectory_write.argtypes = [POINTER(CHRP_TRAJECTORY), POINTER(CHRP_FRAME)]
c_lib.chrp_trajectory_write.restype = c_int
c_lib.chrp_trajectory_write.errcheck = _check

# Function "chrp_trajectory_set_topology", at chemharp.h:151
c_lib.chrp_trajectory_set_topology.argtypes = [POINTER(CHRP_TRAJECTORY), POINTER(CHRP_TOPOLOGY)]
c_lib.chrp_trajectory_set_topology.restype = c_int
c_lib.chrp_trajectory_set_topology.errcheck = _check

# Function "chrp_trajectory_set_topology_file", at chemharp.h:160
c_lib.chrp_trajectory_set_topology_file.argtypes = [POINTER(CHRP_TRAJECTORY), c_char_p]
c_lib.chrp_trajectory_set_topology_file.restype = c_int
c_lib.chrp_trajectory_set_topology_file.errcheck = _check

# Function "chrp_trajectory_set_cell", at chemharp.h:170
c_lib.chrp_trajectory_set_cell.argtypes = [POINTER(CHRP_TRAJECTORY), POINTER(CHRP_CELL)]
c_lib.chrp_trajectory_set_cell.restype = c_int
c_lib.chrp_trajectory_set_cell.errcheck = _check

# Function "chrp_trajectory_nsteps", at chemharp.h:178
c_lib.chrp_trajectory_nsteps.argtypes = [POINTER(CHRP_TRAJECTORY), POINTER(c_size_t)]
c_lib.chrp_trajectory_nsteps.restype = c_int
c_lib.chrp_trajectory_nsteps.errcheck = _check

# Function "chrp_trajectory_close", at chemharp.h:186
c_lib.chrp_trajectory_close.argtypes = [POINTER(CHRP_TRAJECTORY)]
c_lib.chrp_trajectory_close.restype = c_int
c_lib.chrp_trajectory_close.errcheck = _check

# Function "chrp_frame", at chemharp.h:195
c_lib.chrp_frame.argtypes = [c_size_t]
c_lib.chrp_frame.restype = POINTER(CHRP_FRAME)


# Function "chrp_frame_atoms_count", at chemharp.h:203
c_lib.chrp_frame_atoms_count.argtypes = [POINTER(CHRP_FRAME), POINTER(c_size_t)]
c_lib.chrp_frame_atoms_count.restype = c_int
c_lib.chrp_frame_atoms_count.errcheck = _check

# Function "chrp_frame_positions", at chemharp.h:212
c_lib.chrp_frame_positions.argtypes = [POINTER(CHRP_FRAME), ndpointer(np.float32, flags="C_CONTIGUOUS", ndim=2), c_size_t]
c_lib.chrp_frame_positions.restype = c_int
c_lib.chrp_frame_positions.errcheck = _check

# Function "chrp_frame_set_positions", at chemharp.h:221
c_lib.chrp_frame_set_positions.argtypes = [POINTER(CHRP_FRAME), ndpointer(np.float32, flags="C_CONTIGUOUS", ndim=2), c_size_t]
c_lib.chrp_frame_set_positions.restype = c_int
c_lib.chrp_frame_set_positions.errcheck = _check

# Function "chrp_frame_velocities", at chemharp.h:230
c_lib.chrp_frame_velocities.argtypes = [POINTER(CHRP_FRAME), ndpointer(np.float32, flags="C_CONTIGUOUS", ndim=2), c_size_t]
c_lib.chrp_frame_velocities.restype = c_int
c_lib.chrp_frame_velocities.errcheck = _check

# Function "chrp_frame_set_velocities", at chemharp.h:239
c_lib.chrp_frame_set_velocities.argtypes = [POINTER(CHRP_FRAME), ndpointer(np.float32, flags="C_CONTIGUOUS", ndim=2), c_size_t]
c_lib.chrp_frame_set_velocities.restype = c_int
c_lib.chrp_frame_set_velocities.errcheck = _check

# Function "chrp_frame_has_velocities", at chemharp.h:247
c_lib.chrp_frame_has_velocities.argtypes = [POINTER(CHRP_FRAME), POINTER(c_bool)]
c_lib.chrp_frame_has_velocities.restype = c_int
c_lib.chrp_frame_has_velocities.errcheck = _check

# Function "chrp_frame_set_cell", at chemharp.h:255
c_lib.chrp_frame_set_cell.argtypes = [POINTER(CHRP_FRAME), POINTER(CHRP_CELL)]
c_lib.chrp_frame_set_cell.restype = c_int
c_lib.chrp_frame_set_cell.errcheck = _check

# Function "chrp_frame_set_topology", at chemharp.h:263
c_lib.chrp_frame_set_topology.argtypes = [POINTER(CHRP_FRAME), POINTER(CHRP_TOPOLOGY)]
c_lib.chrp_frame_set_topology.restype = c_int
c_lib.chrp_frame_set_topology.errcheck = _check

# Function "chrp_frame_step", at chemharp.h:271
c_lib.chrp_frame_step.argtypes = [POINTER(CHRP_FRAME), POINTER(c_size_t)]
c_lib.chrp_frame_step.restype = c_int
c_lib.chrp_frame_step.errcheck = _check

# Function "chrp_frame_set_step", at chemharp.h:279
c_lib.chrp_frame_set_step.argtypes = [POINTER(CHRP_FRAME), c_size_t]
c_lib.chrp_frame_set_step.restype = c_int
c_lib.chrp_frame_set_step.errcheck = _check

# Function "chrp_frame_guess_topology", at chemharp.h:289
c_lib.chrp_frame_guess_topology.argtypes = [POINTER(CHRP_FRAME), c_bool]
c_lib.chrp_frame_guess_topology.restype = c_int
c_lib.chrp_frame_guess_topology.errcheck = _check

# Function "chrp_frame_free", at chemharp.h:296
c_lib.chrp_frame_free.argtypes = [POINTER(CHRP_FRAME)]
c_lib.chrp_frame_free.restype = c_int
c_lib.chrp_frame_free.errcheck = _check

# Function "chrp_cell", at chemharp.h:304
c_lib.chrp_cell.argtypes = [c_double, c_double, c_double]
c_lib.chrp_cell.restype = POINTER(CHRP_CELL)


# Function "chrp_cell_triclinic", at chemharp.h:312
c_lib.chrp_cell_triclinic.argtypes = [c_double, c_double, c_double, c_double, c_double, c_double]
c_lib.chrp_cell_triclinic.restype = POINTER(CHRP_CELL)


# Function "chrp_cell_from_frame", at chemharp.h:319
c_lib.chrp_cell_from_frame.argtypes = [POINTER(CHRP_FRAME)]
c_lib.chrp_cell_from_frame.restype = POINTER(CHRP_CELL)


# Function "chrp_cell_volume", at chemharp.h:327
c_lib.chrp_cell_volume.argtypes = [POINTER(CHRP_CELL), POINTER(c_double)]
c_lib.chrp_cell_volume.restype = c_int
c_lib.chrp_cell_volume.errcheck = _check

# Function "chrp_cell_lengths", at chemharp.h:335
c_lib.chrp_cell_lengths.argtypes = [POINTER(CHRP_CELL), POINTER(c_double), POINTER(c_double), POINTER(c_double)]
c_lib.chrp_cell_lengths.restype = c_int
c_lib.chrp_cell_lengths.errcheck = _check

# Function "chrp_cell_set_lengths", at chemharp.h:343
c_lib.chrp_cell_set_lengths.argtypes = [POINTER(CHRP_CELL), c_double, c_double, c_double]
c_lib.chrp_cell_set_lengths.restype = c_int
c_lib.chrp_cell_set_lengths.errcheck = _check

# Function "chrp_cell_angles", at chemharp.h:351
c_lib.chrp_cell_angles.argtypes = [POINTER(CHRP_CELL), POINTER(c_double), POINTER(c_double), POINTER(c_double)]
c_lib.chrp_cell_angles.restype = c_int
c_lib.chrp_cell_angles.errcheck = _check

# Function "chrp_cell_set_angles", at chemharp.h:359
c_lib.chrp_cell_set_angles.argtypes = [POINTER(CHRP_CELL), c_double, c_double, c_double]
c_lib.chrp_cell_set_angles.restype = c_int
c_lib.chrp_cell_set_angles.errcheck = _check

# Function "chrp_cell_matrix", at chemharp.h:367
c_lib.chrp_cell_matrix.argtypes = [POINTER(CHRP_CELL), ndpointer(np.float64, flags="C_CONTIGUOUS", ndim=2, shape=(3, 3))]
c_lib.chrp_cell_matrix.restype = c_int
c_lib.chrp_cell_matrix.errcheck = _check

# Function "chrp_cell_type", at chemharp.h:385
c_lib.chrp_cell_type.argtypes = [POINTER(CHRP_CELL), POINTER(c_int)]
c_lib.chrp_cell_type.restype = c_int
c_lib.chrp_cell_type.errcheck = _check

# Function "chrp_cell_set_type", at chemharp.h:393
c_lib.chrp_cell_set_type.argtypes = [POINTER(CHRP_CELL), c_int]
c_lib.chrp_cell_set_type.restype = c_int
c_lib.chrp_cell_set_type.errcheck = _check

# Function "chrp_cell_periodicity", at chemharp.h:401
c_lib.chrp_cell_periodicity.argtypes = [POINTER(CHRP_CELL), POINTER(c_bool), POINTER(c_bool), POINTER(c_bool)]
c_lib.chrp_cell_periodicity.restype = c_int
c_lib.chrp_cell_periodicity.errcheck = _check

# Function "chrp_cell_set_periodicity", at chemharp.h:409
c_lib.chrp_cell_set_periodicity.argtypes = [POINTER(CHRP_CELL), c_bool, c_bool, c_bool]
c_lib.chrp_cell_set_periodicity.restype = c_int
c_lib.chrp_cell_set_periodicity.errcheck = _check

# Function "chrp_cell_free", at chemharp.h:416
c_lib.chrp_cell_free.argtypes = [POINTER(CHRP_CELL)]
c_lib.chrp_cell_free.restype = c_int
c_lib.chrp_cell_free.errcheck = _check

# Function "chrp_topology", at chemharp.h:424
c_lib.chrp_topology.argtypes = []
c_lib.chrp_topology.restype = POINTER(CHRP_TOPOLOGY)


# Function "chrp_topology_from_frame", at chemharp.h:431
c_lib.chrp_topology_from_frame.argtypes = [POINTER(CHRP_FRAME)]
c_lib.chrp_topology_from_frame.restype = POINTER(CHRP_TOPOLOGY)


# Function "chrp_topology_atoms_count", at chemharp.h:439
c_lib.chrp_topology_atoms_count.argtypes = [POINTER(CHRP_TOPOLOGY), POINTER(c_size_t)]
c_lib.chrp_topology_atoms_count.restype = c_int
c_lib.chrp_topology_atoms_count.errcheck = _check

# Function "chrp_topology_append", at chemharp.h:447
c_lib.chrp_topology_append.argtypes = [POINTER(CHRP_TOPOLOGY), POINTER(CHRP_ATOM)]
c_lib.chrp_topology_append.restype = c_int
c_lib.chrp_topology_append.errcheck = _check

# Function "chrp_topology_remove", at chemharp.h:455
c_lib.chrp_topology_remove.argtypes = [POINTER(CHRP_TOPOLOGY), c_size_t]
c_lib.chrp_topology_remove.restype = c_int
c_lib.chrp_topology_remove.errcheck = _check

# Function "chrp_topology_isbond", at chemharp.h:464
c_lib.chrp_topology_isbond.argtypes = [POINTER(CHRP_TOPOLOGY), c_size_t, c_size_t, POINTER(c_bool)]
c_lib.chrp_topology_isbond.restype = c_int
c_lib.chrp_topology_isbond.errcheck = _check

# Function "chrp_topology_isangle", at chemharp.h:473
c_lib.chrp_topology_isangle.argtypes = [POINTER(CHRP_TOPOLOGY), c_size_t, c_size_t, c_size_t, POINTER(c_bool)]
c_lib.chrp_topology_isangle.restype = c_int
c_lib.chrp_topology_isangle.errcheck = _check

# Function "chrp_topology_isdihedral", at chemharp.h:482
c_lib.chrp_topology_isdihedral.argtypes = [POINTER(CHRP_TOPOLOGY), c_size_t, c_size_t, c_size_t, c_size_t, POINTER(c_bool)]
c_lib.chrp_topology_isdihedral.restype = c_int
c_lib.chrp_topology_isdihedral.errcheck = _check

# Function "chrp_topology_bonds_count", at chemharp.h:490
c_lib.chrp_topology_bonds_count.argtypes = [POINTER(CHRP_TOPOLOGY), POINTER(c_size_t)]
c_lib.chrp_topology_bonds_count.restype = c_int
c_lib.chrp_topology_bonds_count.errcheck = _check

# Function "chrp_topology_angles_count", at chemharp.h:498
c_lib.chrp_topology_angles_count.argtypes = [POINTER(CHRP_TOPOLOGY), POINTER(c_size_t)]
c_lib.chrp_topology_angles_count.restype = c_int
c_lib.chrp_topology_angles_count.errcheck = _check

# Function "chrp_topology_dihedrals_count", at chemharp.h:506
c_lib.chrp_topology_dihedrals_count.argtypes = [POINTER(CHRP_TOPOLOGY), POINTER(c_size_t)]
c_lib.chrp_topology_dihedrals_count.restype = c_int
c_lib.chrp_topology_dihedrals_count.errcheck = _check

# Function "chrp_topology_bonds", at chemharp.h:516
c_lib.chrp_topology_bonds.argtypes = [POINTER(CHRP_TOPOLOGY), ndpointer(np.uintp, flags="C_CONTIGUOUS", ndim=2), c_size_t]
c_lib.chrp_topology_bonds.restype = c_int
c_lib.chrp_topology_bonds.errcheck = _check

# Function "chrp_topology_angles", at chemharp.h:526
c_lib.chrp_topology_angles.argtypes = [POINTER(CHRP_TOPOLOGY), ndpointer(np.uintp, flags="C_CONTIGUOUS", ndim=2), c_size_t]
c_lib.chrp_topology_angles.restype = c_int
c_lib.chrp_topology_angles.errcheck = _check

# Function "chrp_topology_dihedrals", at chemharp.h:536
c_lib.chrp_topology_dihedrals.argtypes = [POINTER(CHRP_TOPOLOGY), ndpointer(np.uintp, flags="C_CONTIGUOUS", ndim=2), c_size_t]
c_lib.chrp_topology_dihedrals.restype = c_int
c_lib.chrp_topology_dihedrals.errcheck = _check

# Function "chrp_topology_add_bond", at chemharp.h:544
c_lib.chrp_topology_add_bond.argtypes = [POINTER(CHRP_TOPOLOGY), c_size_t, c_size_t]
c_lib.chrp_topology_add_bond.restype = c_int
c_lib.chrp_topology_add_bond.errcheck = _check

# Function "chrp_topology_remove_bond", at chemharp.h:552
c_lib.chrp_topology_remove_bond.argtypes = [POINTER(CHRP_TOPOLOGY), c_size_t, c_size_t]
c_lib.chrp_topology_remove_bond.restype = c_int
c_lib.chrp_topology_remove_bond.errcheck = _check

# Function "chrp_topology_free", at chemharp.h:559
c_lib.chrp_topology_free.argtypes = [POINTER(CHRP_TOPOLOGY)]
c_lib.chrp_topology_free.restype = c_int
c_lib.chrp_topology_free.errcheck = _check

# Function "chrp_atom", at chemharp.h:568
c_lib.chrp_atom.argtypes = [c_char_p]
c_lib.chrp_atom.restype = POINTER(CHRP_ATOM)


# Function "chrp_atom_from_frame", at chemharp.h:576
c_lib.chrp_atom_from_frame.argtypes = [POINTER(CHRP_FRAME), c_size_t]
c_lib.chrp_atom_from_frame.restype = POINTER(CHRP_ATOM)


# Function "chrp_atom_from_topology", at chemharp.h:584
c_lib.chrp_atom_from_topology.argtypes = [POINTER(CHRP_TOPOLOGY), c_size_t]
c_lib.chrp_atom_from_topology.restype = POINTER(CHRP_ATOM)


# Function "chrp_atom_mass", at chemharp.h:592
c_lib.chrp_atom_mass.argtypes = [POINTER(CHRP_ATOM), POINTER(c_float)]
c_lib.chrp_atom_mass.restype = c_int
c_lib.chrp_atom_mass.errcheck = _check

# Function "chrp_atom_set_mass", at chemharp.h:600
c_lib.chrp_atom_set_mass.argtypes = [POINTER(CHRP_ATOM), c_float]
c_lib.chrp_atom_set_mass.restype = c_int
c_lib.chrp_atom_set_mass.errcheck = _check

# Function "chrp_atom_charge", at chemharp.h:608
c_lib.chrp_atom_charge.argtypes = [POINTER(CHRP_ATOM), POINTER(c_float)]
c_lib.chrp_atom_charge.restype = c_int
c_lib.chrp_atom_charge.errcheck = _check

# Function "chrp_atom_set_charge", at chemharp.h:616
c_lib.chrp_atom_set_charge.argtypes = [POINTER(CHRP_ATOM), c_float]
c_lib.chrp_atom_set_charge.restype = c_int
c_lib.chrp_atom_set_charge.errcheck = _check

# Function "chrp_atom_name", at chemharp.h:625
c_lib.chrp_atom_name.argtypes = [POINTER(CHRP_ATOM), c_char_p, c_size_t]
c_lib.chrp_atom_name.restype = c_int
c_lib.chrp_atom_name.errcheck = _check

# Function "chrp_atom_set_name", at chemharp.h:633
c_lib.chrp_atom_set_name.argtypes = [POINTER(CHRP_ATOM), c_char_p]
c_lib.chrp_atom_set_name.restype = c_int
c_lib.chrp_atom_set_name.errcheck = _check

# Function "chrp_atom_full_name", at chemharp.h:642
c_lib.chrp_atom_full_name.argtypes = [POINTER(CHRP_ATOM), c_char_p, c_size_t]
c_lib.chrp_atom_full_name.restype = c_int
c_lib.chrp_atom_full_name.errcheck = _check

# Function "chrp_atom_vdw_radius", at chemharp.h:650
c_lib.chrp_atom_vdw_radius.argtypes = [POINTER(CHRP_ATOM), POINTER(c_double)]
c_lib.chrp_atom_vdw_radius.restype = c_int
c_lib.chrp_atom_vdw_radius.errcheck = _check

# Function "chrp_atom_covalent_radius", at chemharp.h:658
c_lib.chrp_atom_covalent_radius.argtypes = [POINTER(CHRP_ATOM), POINTER(c_double)]
c_lib.chrp_atom_covalent_radius.restype = c_int
c_lib.chrp_atom_covalent_radius.errcheck = _check

# Function "chrp_atom_atomic_number", at chemharp.h:666
c_lib.chrp_atom_atomic_number.argtypes = [POINTER(CHRP_ATOM), POINTER(c_int)]
c_lib.chrp_atom_atomic_number.restype = c_int
c_lib.chrp_atom_atomic_number.errcheck = _check

# Function "chrp_atom_free", at chemharp.h:673
c_lib.chrp_atom_free.argtypes = [POINTER(CHRP_ATOM)]
c_lib.chrp_atom_free.restype = c_int
c_lib.chrp_atom_free.errcheck = _check