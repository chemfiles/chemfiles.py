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

# flake8: noqa
'''
Foreign function interface declaration for the Python interface to chemfiles
'''
from numpy.ctypeslib import ndpointer
import numpy as np
from ctypes import *

from .errors import _check_return_code


class CHFL_LOG_LEVEL(c_int):
    CHFL_LOG_ERROR = 0
    CHFL_LOG_WARNING = 1
    CHFL_LOG_INFO = 2
    CHFL_LOG_DEBUG = 3


class CHFL_CELL_TYPES(c_int):
    CHFL_CELL_ORTHORHOMBIC = 0
    CHFL_CELL_TRICLINIC = 1
    CHFL_CELL_INFINITE = 2


class CHFL_ATOM_TYPES(c_int):
    CHFL_ATOM_ELEMENT = 0
    CHFL_ATOM_COARSE_GRAINED = 1
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


class CHFL_SELECTION(Structure):
    pass


class chfl_match_t(Structure):
    _fields_ = [
        ('size', c_int8),
        ('atoms', ARRAY(c_size_t, 4))
    ]


chfl_logging_callback_t = CFUNCTYPE(None, CHFL_LOG_LEVEL, c_char_p)


def set_interface(c_lib):
    # Function "chfl_version", at chemfiles.h:81
    c_lib.chfl_version.argtypes = []
    c_lib.chfl_version.restype = c_char_p

    # Function "chfl_strerror", at chemfiles.h:89
    c_lib.chfl_strerror.argtypes = [c_int]
    c_lib.chfl_strerror.restype = c_char_p

    # Function "chfl_last_error", at chemfiles.h:96
    c_lib.chfl_last_error.argtypes = []
    c_lib.chfl_last_error.restype = c_char_p

    # Function "chfl_clear_errors", at chemfiles.h:102
    c_lib.chfl_clear_errors.argtypes = []
    c_lib.chfl_clear_errors.restype = c_int
    c_lib.chfl_clear_errors.errcheck = _check_return_code

    # Function "chfl_loglevel", at chemfiles.h:121
    c_lib.chfl_loglevel.argtypes = [POINTER(c_int)]
    c_lib.chfl_loglevel.restype = c_int
    c_lib.chfl_loglevel.errcheck = _check_return_code

    # Function "chfl_set_loglevel", at chemfiles.h:128
    c_lib.chfl_set_loglevel.argtypes = [c_int]
    c_lib.chfl_set_loglevel.restype = c_int
    c_lib.chfl_set_loglevel.errcheck = _check_return_code

    # Function "chfl_logfile", at chemfiles.h:135
    c_lib.chfl_logfile.argtypes = [c_char_p]
    c_lib.chfl_logfile.restype = c_int
    c_lib.chfl_logfile.errcheck = _check_return_code

    # Function "chfl_log_stdout", at chemfiles.h:141
    c_lib.chfl_log_stdout.argtypes = []
    c_lib.chfl_log_stdout.restype = c_int
    c_lib.chfl_log_stdout.errcheck = _check_return_code

    # Function "chfl_log_stderr", at chemfiles.h:148
    c_lib.chfl_log_stderr.argtypes = []
    c_lib.chfl_log_stderr.restype = c_int
    c_lib.chfl_log_stderr.errcheck = _check_return_code

    # Function "chfl_log_silent", at chemfiles.h:154
    c_lib.chfl_log_silent.argtypes = []
    c_lib.chfl_log_silent.restype = c_int
    c_lib.chfl_log_silent.errcheck = _check_return_code

    # Function "chfl_log_callback", at chemfiles.h:165
    c_lib.chfl_log_callback.argtypes = [chfl_logging_callback_t]
    c_lib.chfl_log_callback.restype = c_int
    c_lib.chfl_log_callback.errcheck = _check_return_code

    # Function "chfl_trajectory_open", at chemfiles.h:174
    c_lib.chfl_trajectory_open.argtypes = [c_char_p, c_char]
    c_lib.chfl_trajectory_open.restype = POINTER(CHFL_TRAJECTORY)

    # Function "chfl_trajectory_with_format", at chemfiles.h:188
    c_lib.chfl_trajectory_with_format.argtypes = [c_char_p, c_char, c_char_p]
    c_lib.chfl_trajectory_with_format.restype = POINTER(CHFL_TRAJECTORY)

    # Function "chfl_trajectory_read", at chemfiles.h:198
    c_lib.chfl_trajectory_read.argtypes = [POINTER(CHFL_TRAJECTORY), POINTER(CHFL_FRAME)]
    c_lib.chfl_trajectory_read.restype = c_int
    c_lib.chfl_trajectory_read.errcheck = _check_return_code

    # Function "chfl_trajectory_read_step", at chemfiles.h:207
    c_lib.chfl_trajectory_read_step.argtypes = [POINTER(CHFL_TRAJECTORY), c_size_t, POINTER(CHFL_FRAME)]
    c_lib.chfl_trajectory_read_step.restype = c_int
    c_lib.chfl_trajectory_read_step.errcheck = _check_return_code

    # Function "chfl_trajectory_write", at chemfiles.h:217
    c_lib.chfl_trajectory_write.argtypes = [POINTER(CHFL_TRAJECTORY), POINTER(CHFL_FRAME)]
    c_lib.chfl_trajectory_write.restype = c_int
    c_lib.chfl_trajectory_write.errcheck = _check_return_code

    # Function "chfl_trajectory_set_topology", at chemfiles.h:228
    c_lib.chfl_trajectory_set_topology.argtypes = [POINTER(CHFL_TRAJECTORY), POINTER(CHFL_TOPOLOGY)]
    c_lib.chfl_trajectory_set_topology.restype = c_int
    c_lib.chfl_trajectory_set_topology.errcheck = _check_return_code

    # Function "chfl_trajectory_set_topology_file", at chemfiles.h:238
    c_lib.chfl_trajectory_set_topology_file.argtypes = [POINTER(CHFL_TRAJECTORY), c_char_p]
    c_lib.chfl_trajectory_set_topology_file.restype = c_int
    c_lib.chfl_trajectory_set_topology_file.errcheck = _check_return_code

    # Function "chfl_trajectory_set_topology_with_format", at chemfiles.h:256
    c_lib.chfl_trajectory_set_topology_with_format.argtypes = [POINTER(CHFL_TRAJECTORY), c_char_p, c_char_p]
    c_lib.chfl_trajectory_set_topology_with_format.restype = c_int
    c_lib.chfl_trajectory_set_topology_with_format.errcheck = _check_return_code

    # Function "chfl_trajectory_set_cell", at chemfiles.h:268
    c_lib.chfl_trajectory_set_cell.argtypes = [POINTER(CHFL_TRAJECTORY), POINTER(CHFL_CELL)]
    c_lib.chfl_trajectory_set_cell.restype = c_int
    c_lib.chfl_trajectory_set_cell.errcheck = _check_return_code

    # Function "chfl_trajectory_nsteps", at chemfiles.h:277
    c_lib.chfl_trajectory_nsteps.argtypes = [POINTER(CHFL_TRAJECTORY), POINTER(c_size_t)]
    c_lib.chfl_trajectory_nsteps.restype = c_int
    c_lib.chfl_trajectory_nsteps.errcheck = _check_return_code

    # Function "chfl_trajectory_sync", at chemfiles.h:284
    c_lib.chfl_trajectory_sync.argtypes = [POINTER(CHFL_TRAJECTORY)]
    c_lib.chfl_trajectory_sync.restype = c_int
    c_lib.chfl_trajectory_sync.errcheck = _check_return_code

    # Function "chfl_trajectory_close", at chemfiles.h:291
    c_lib.chfl_trajectory_close.argtypes = [POINTER(CHFL_TRAJECTORY)]
    c_lib.chfl_trajectory_close.restype = c_int
    c_lib.chfl_trajectory_close.errcheck = _check_return_code

    # Function "chfl_frame", at chemfiles.h:300
    c_lib.chfl_frame.argtypes = [c_size_t]
    c_lib.chfl_frame.restype = POINTER(CHFL_FRAME)

    # Function "chfl_frame_atoms_count", at chemfiles.h:308
    c_lib.chfl_frame_atoms_count.argtypes = [POINTER(CHFL_FRAME), POINTER(c_size_t)]
    c_lib.chfl_frame_atoms_count.restype = c_int
    c_lib.chfl_frame_atoms_count.errcheck = _check_return_code

    # Function "chfl_frame_positions", at chemfiles.h:325
    c_lib.chfl_frame_positions.argtypes = [POINTER(CHFL_FRAME), POINTER(POINTER(c_float)), POINTER(c_size_t)]
    c_lib.chfl_frame_positions.restype = c_int
    c_lib.chfl_frame_positions.errcheck = _check_return_code

    # Function "chfl_frame_velocities", at chemfiles.h:346
    c_lib.chfl_frame_velocities.argtypes = [POINTER(CHFL_FRAME), POINTER(POINTER(c_float)), POINTER(c_size_t)]
    c_lib.chfl_frame_velocities.restype = c_int
    c_lib.chfl_frame_velocities.errcheck = _check_return_code

    # Function "chfl_frame_resize", at chemfiles.h:361
    c_lib.chfl_frame_resize.argtypes = [POINTER(CHFL_FRAME), c_size_t]
    c_lib.chfl_frame_resize.restype = c_int
    c_lib.chfl_frame_resize.errcheck = _check_return_code

    # Function "chfl_frame_add_velocities", at chemfiles.h:372
    c_lib.chfl_frame_add_velocities.argtypes = [POINTER(CHFL_FRAME)]
    c_lib.chfl_frame_add_velocities.restype = c_int
    c_lib.chfl_frame_add_velocities.errcheck = _check_return_code

    # Function "chfl_frame_has_velocities", at chemfiles.h:381
    c_lib.chfl_frame_has_velocities.argtypes = [POINTER(CHFL_FRAME), POINTER(c_bool)]
    c_lib.chfl_frame_has_velocities.restype = c_int
    c_lib.chfl_frame_has_velocities.errcheck = _check_return_code

    # Function "chfl_frame_set_cell", at chemfiles.h:390
    c_lib.chfl_frame_set_cell.argtypes = [POINTER(CHFL_FRAME), POINTER(CHFL_CELL)]
    c_lib.chfl_frame_set_cell.restype = c_int
    c_lib.chfl_frame_set_cell.errcheck = _check_return_code

    # Function "chfl_frame_set_topology", at chemfiles.h:398
    c_lib.chfl_frame_set_topology.argtypes = [POINTER(CHFL_FRAME), POINTER(CHFL_TOPOLOGY)]
    c_lib.chfl_frame_set_topology.restype = c_int
    c_lib.chfl_frame_set_topology.errcheck = _check_return_code

    # Function "chfl_frame_step", at chemfiles.h:407
    c_lib.chfl_frame_step.argtypes = [POINTER(CHFL_FRAME), POINTER(c_size_t)]
    c_lib.chfl_frame_step.restype = c_int
    c_lib.chfl_frame_step.errcheck = _check_return_code

    # Function "chfl_frame_set_step", at chemfiles.h:415
    c_lib.chfl_frame_set_step.argtypes = [POINTER(CHFL_FRAME), c_size_t]
    c_lib.chfl_frame_set_step.restype = c_int
    c_lib.chfl_frame_set_step.errcheck = _check_return_code

    # Function "chfl_frame_guess_topology", at chemfiles.h:426
    c_lib.chfl_frame_guess_topology.argtypes = [POINTER(CHFL_FRAME)]
    c_lib.chfl_frame_guess_topology.restype = c_int
    c_lib.chfl_frame_guess_topology.errcheck = _check_return_code

    # Function "chfl_frame_free", at chemfiles.h:433
    c_lib.chfl_frame_free.argtypes = [POINTER(CHFL_FRAME)]
    c_lib.chfl_frame_free.restype = c_int
    c_lib.chfl_frame_free.errcheck = _check_return_code

    # Function "chfl_cell", at chemfiles.h:443
    c_lib.chfl_cell.argtypes = [c_double, c_double, c_double]
    c_lib.chfl_cell.restype = POINTER(CHFL_CELL)

    # Function "chfl_cell_triclinic", at chemfiles.h:455
    c_lib.chfl_cell_triclinic.argtypes = [c_double, c_double, c_double, c_double, c_double, c_double]
    c_lib.chfl_cell_triclinic.restype = POINTER(CHFL_CELL)

    # Function "chfl_cell_from_frame", at chemfiles.h:463
    c_lib.chfl_cell_from_frame.argtypes = [POINTER(CHFL_FRAME)]
    c_lib.chfl_cell_from_frame.restype = POINTER(CHFL_CELL)

    # Function "chfl_cell_volume", at chemfiles.h:471
    c_lib.chfl_cell_volume.argtypes = [POINTER(CHFL_CELL), POINTER(c_double)]
    c_lib.chfl_cell_volume.restype = c_int
    c_lib.chfl_cell_volume.errcheck = _check_return_code

    # Function "chfl_cell_lengths", at chemfiles.h:482
    c_lib.chfl_cell_lengths.argtypes = [POINTER(CHFL_CELL), POINTER(c_double), POINTER(c_double), POINTER(c_double)]
    c_lib.chfl_cell_lengths.restype = c_int
    c_lib.chfl_cell_lengths.errcheck = _check_return_code

    # Function "chfl_cell_set_lengths", at chemfiles.h:493
    c_lib.chfl_cell_set_lengths.argtypes = [POINTER(CHFL_CELL), c_double, c_double, c_double]
    c_lib.chfl_cell_set_lengths.restype = c_int
    c_lib.chfl_cell_set_lengths.errcheck = _check_return_code

    # Function "chfl_cell_angles", at chemfiles.h:503
    c_lib.chfl_cell_angles.argtypes = [POINTER(CHFL_CELL), POINTER(c_double), POINTER(c_double), POINTER(c_double)]
    c_lib.chfl_cell_angles.restype = c_int
    c_lib.chfl_cell_angles.errcheck = _check_return_code

    # Function "chfl_cell_set_angles", at chemfiles.h:518
    c_lib.chfl_cell_set_angles.argtypes = [POINTER(CHFL_CELL), c_double, c_double, c_double]
    c_lib.chfl_cell_set_angles.restype = c_int
    c_lib.chfl_cell_set_angles.errcheck = _check_return_code

    # Function "chfl_cell_matrix", at chemfiles.h:526
    c_lib.chfl_cell_matrix.argtypes = [POINTER(CHFL_CELL), ndpointer(np.float64, flags="C_CONTIGUOUS", ndim=2)]
    c_lib.chfl_cell_matrix.restype = c_int
    c_lib.chfl_cell_matrix.errcheck = _check_return_code

    # Function "chfl_cell_type", at chemfiles.h:544
    c_lib.chfl_cell_type.argtypes = [POINTER(CHFL_CELL), POINTER(c_int)]
    c_lib.chfl_cell_type.restype = c_int
    c_lib.chfl_cell_type.errcheck = _check_return_code

    # Function "chfl_cell_set_type", at chemfiles.h:552
    c_lib.chfl_cell_set_type.argtypes = [POINTER(CHFL_CELL), c_int]
    c_lib.chfl_cell_set_type.restype = c_int
    c_lib.chfl_cell_set_type.errcheck = _check_return_code

    # Function "chfl_cell_free", at chemfiles.h:559
    c_lib.chfl_cell_free.argtypes = [POINTER(CHFL_CELL)]
    c_lib.chfl_cell_free.restype = c_int
    c_lib.chfl_cell_free.errcheck = _check_return_code

    # Function "chfl_topology", at chemfiles.h:567
    c_lib.chfl_topology.argtypes = []
    c_lib.chfl_topology.restype = POINTER(CHFL_TOPOLOGY)

    # Function "chfl_topology_from_frame", at chemfiles.h:574
    c_lib.chfl_topology_from_frame.argtypes = [POINTER(CHFL_FRAME)]
    c_lib.chfl_topology_from_frame.restype = POINTER(CHFL_TOPOLOGY)

    # Function "chfl_topology_atoms_count", at chemfiles.h:582
    c_lib.chfl_topology_atoms_count.argtypes = [POINTER(CHFL_TOPOLOGY), POINTER(c_size_t)]
    c_lib.chfl_topology_atoms_count.restype = c_int
    c_lib.chfl_topology_atoms_count.errcheck = _check_return_code

    # Function "chfl_topology_append", at chemfiles.h:591
    c_lib.chfl_topology_append.argtypes = [POINTER(CHFL_TOPOLOGY), POINTER(CHFL_ATOM)]
    c_lib.chfl_topology_append.restype = c_int
    c_lib.chfl_topology_append.errcheck = _check_return_code

    # Function "chfl_topology_remove", at chemfiles.h:601
    c_lib.chfl_topology_remove.argtypes = [POINTER(CHFL_TOPOLOGY), c_size_t]
    c_lib.chfl_topology_remove.restype = c_int
    c_lib.chfl_topology_remove.errcheck = _check_return_code

    # Function "chfl_topology_isbond", at chemfiles.h:611
    c_lib.chfl_topology_isbond.argtypes = [POINTER(CHFL_TOPOLOGY), c_size_t, c_size_t, POINTER(c_bool)]
    c_lib.chfl_topology_isbond.restype = c_int
    c_lib.chfl_topology_isbond.errcheck = _check_return_code

    # Function "chfl_topology_isangle", at chemfiles.h:625
    c_lib.chfl_topology_isangle.argtypes = [POINTER(CHFL_TOPOLOGY), c_size_t, c_size_t, c_size_t, POINTER(c_bool)]
    c_lib.chfl_topology_isangle.restype = c_int
    c_lib.chfl_topology_isangle.errcheck = _check_return_code

    # Function "chfl_topology_isdihedral", at chemfiles.h:638
    c_lib.chfl_topology_isdihedral.argtypes = [POINTER(CHFL_TOPOLOGY), c_size_t, c_size_t, c_size_t, c_size_t, POINTER(c_bool)]
    c_lib.chfl_topology_isdihedral.restype = c_int
    c_lib.chfl_topology_isdihedral.errcheck = _check_return_code

    # Function "chfl_topology_bonds_count", at chemfiles.h:651
    c_lib.chfl_topology_bonds_count.argtypes = [POINTER(CHFL_TOPOLOGY), POINTER(c_size_t)]
    c_lib.chfl_topology_bonds_count.restype = c_int
    c_lib.chfl_topology_bonds_count.errcheck = _check_return_code

    # Function "chfl_topology_angles_count", at chemfiles.h:660
    c_lib.chfl_topology_angles_count.argtypes = [POINTER(CHFL_TOPOLOGY), POINTER(c_size_t)]
    c_lib.chfl_topology_angles_count.restype = c_int
    c_lib.chfl_topology_angles_count.errcheck = _check_return_code

    # Function "chfl_topology_dihedrals_count", at chemfiles.h:669
    c_lib.chfl_topology_dihedrals_count.argtypes = [POINTER(CHFL_TOPOLOGY), POINTER(c_size_t)]
    c_lib.chfl_topology_dihedrals_count.restype = c_int
    c_lib.chfl_topology_dihedrals_count.errcheck = _check_return_code

    # Function "chfl_topology_bonds", at chemfiles.h:680
    c_lib.chfl_topology_bonds.argtypes = [POINTER(CHFL_TOPOLOGY), ndpointer(np.uintp, flags="C_CONTIGUOUS", ndim=2), c_size_t]
    c_lib.chfl_topology_bonds.restype = c_int
    c_lib.chfl_topology_bonds.errcheck = _check_return_code

    # Function "chfl_topology_angles", at chemfiles.h:692
    c_lib.chfl_topology_angles.argtypes = [POINTER(CHFL_TOPOLOGY), ndpointer(np.uintp, flags="C_CONTIGUOUS", ndim=2), c_size_t]
    c_lib.chfl_topology_angles.restype = c_int
    c_lib.chfl_topology_angles.errcheck = _check_return_code

    # Function "chfl_topology_dihedrals", at chemfiles.h:706
    c_lib.chfl_topology_dihedrals.argtypes = [POINTER(CHFL_TOPOLOGY), ndpointer(np.uintp, flags="C_CONTIGUOUS", ndim=2), c_size_t]
    c_lib.chfl_topology_dihedrals.restype = c_int
    c_lib.chfl_topology_dihedrals.errcheck = _check_return_code

    # Function "chfl_topology_add_bond", at chemfiles.h:718
    c_lib.chfl_topology_add_bond.argtypes = [POINTER(CHFL_TOPOLOGY), c_size_t, c_size_t]
    c_lib.chfl_topology_add_bond.restype = c_int
    c_lib.chfl_topology_add_bond.errcheck = _check_return_code

    # Function "chfl_topology_remove_bond", at chemfiles.h:728
    c_lib.chfl_topology_remove_bond.argtypes = [POINTER(CHFL_TOPOLOGY), c_size_t, c_size_t]
    c_lib.chfl_topology_remove_bond.restype = c_int
    c_lib.chfl_topology_remove_bond.errcheck = _check_return_code

    # Function "chfl_topology_free", at chemfiles.h:735
    c_lib.chfl_topology_free.argtypes = [POINTER(CHFL_TOPOLOGY)]
    c_lib.chfl_topology_free.restype = c_int
    c_lib.chfl_topology_free.errcheck = _check_return_code

    # Function "chfl_atom", at chemfiles.h:744
    c_lib.chfl_atom.argtypes = [c_char_p]
    c_lib.chfl_atom.restype = POINTER(CHFL_ATOM)

    # Function "chfl_atom_from_frame", at chemfiles.h:752
    c_lib.chfl_atom_from_frame.argtypes = [POINTER(CHFL_FRAME), c_size_t]
    c_lib.chfl_atom_from_frame.restype = POINTER(CHFL_ATOM)

    # Function "chfl_atom_from_topology", at chemfiles.h:761
    c_lib.chfl_atom_from_topology.argtypes = [POINTER(CHFL_TOPOLOGY), c_size_t]
    c_lib.chfl_atom_from_topology.restype = POINTER(CHFL_ATOM)

    # Function "chfl_atom_mass", at chemfiles.h:770
    c_lib.chfl_atom_mass.argtypes = [POINTER(CHFL_ATOM), POINTER(c_float)]
    c_lib.chfl_atom_mass.restype = c_int
    c_lib.chfl_atom_mass.errcheck = _check_return_code

    # Function "chfl_atom_set_mass", at chemfiles.h:778
    c_lib.chfl_atom_set_mass.argtypes = [POINTER(CHFL_ATOM), c_float]
    c_lib.chfl_atom_set_mass.restype = c_int
    c_lib.chfl_atom_set_mass.errcheck = _check_return_code

    # Function "chfl_atom_charge", at chemfiles.h:786
    c_lib.chfl_atom_charge.argtypes = [POINTER(CHFL_ATOM), POINTER(c_float)]
    c_lib.chfl_atom_charge.restype = c_int
    c_lib.chfl_atom_charge.errcheck = _check_return_code

    # Function "chfl_atom_set_charge", at chemfiles.h:794
    c_lib.chfl_atom_set_charge.argtypes = [POINTER(CHFL_ATOM), c_float]
    c_lib.chfl_atom_set_charge.restype = c_int
    c_lib.chfl_atom_set_charge.errcheck = _check_return_code

    # Function "chfl_atom_name", at chemfiles.h:804
    c_lib.chfl_atom_name.argtypes = [POINTER(CHFL_ATOM), c_char_p, c_size_t]
    c_lib.chfl_atom_name.restype = c_int
    c_lib.chfl_atom_name.errcheck = _check_return_code

    # Function "chfl_atom_set_name", at chemfiles.h:812
    c_lib.chfl_atom_set_name.argtypes = [POINTER(CHFL_ATOM), c_char_p]
    c_lib.chfl_atom_set_name.restype = c_int
    c_lib.chfl_atom_set_name.errcheck = _check_return_code

    # Function "chfl_atom_full_name", at chemfiles.h:822
    c_lib.chfl_atom_full_name.argtypes = [POINTER(CHFL_ATOM), c_char_p, c_size_t]
    c_lib.chfl_atom_full_name.restype = c_int
    c_lib.chfl_atom_full_name.errcheck = _check_return_code

    # Function "chfl_atom_vdw_radius", at chemfiles.h:831
    c_lib.chfl_atom_vdw_radius.argtypes = [POINTER(CHFL_ATOM), POINTER(c_double)]
    c_lib.chfl_atom_vdw_radius.restype = c_int
    c_lib.chfl_atom_vdw_radius.errcheck = _check_return_code

    # Function "chfl_atom_covalent_radius", at chemfiles.h:840
    c_lib.chfl_atom_covalent_radius.argtypes = [POINTER(CHFL_ATOM), POINTER(c_double)]
    c_lib.chfl_atom_covalent_radius.restype = c_int
    c_lib.chfl_atom_covalent_radius.errcheck = _check_return_code

    # Function "chfl_atom_atomic_number", at chemfiles.h:849
    c_lib.chfl_atom_atomic_number.argtypes = [POINTER(CHFL_ATOM), POINTER(c_int)]
    c_lib.chfl_atom_atomic_number.restype = c_int
    c_lib.chfl_atom_atomic_number.errcheck = _check_return_code

    # Function "chfl_atom_type", at chemfiles.h:870
    c_lib.chfl_atom_type.argtypes = [POINTER(CHFL_ATOM), POINTER(c_int)]
    c_lib.chfl_atom_type.restype = c_int
    c_lib.chfl_atom_type.errcheck = _check_return_code

    # Function "chfl_atom_set_type", at chemfiles.h:878
    c_lib.chfl_atom_set_type.argtypes = [POINTER(CHFL_ATOM), c_int]
    c_lib.chfl_atom_set_type.restype = c_int
    c_lib.chfl_atom_set_type.errcheck = _check_return_code

    # Function "chfl_atom_free", at chemfiles.h:885
    c_lib.chfl_atom_free.argtypes = [POINTER(CHFL_ATOM)]
    c_lib.chfl_atom_free.restype = c_int
    c_lib.chfl_atom_free.errcheck = _check_return_code

    # Function "chfl_selection", at chemfiles.h:893
    c_lib.chfl_selection.argtypes = [c_char_p]
    c_lib.chfl_selection.restype = POINTER(CHFL_SELECTION)

    # Function "chfl_selection_size", at chemfiles.h:907
    c_lib.chfl_selection_size.argtypes = [POINTER(CHFL_SELECTION), POINTER(c_size_t)]
    c_lib.chfl_selection_size.restype = c_int
    c_lib.chfl_selection_size.errcheck = _check_return_code

    # Function "chfl_selection_evalutate", at chemfiles.h:919
    c_lib.chfl_selection_evalutate.argtypes = [POINTER(CHFL_SELECTION), POINTER(CHFL_FRAME), POINTER(c_size_t)]
    c_lib.chfl_selection_evalutate.restype = c_int
    c_lib.chfl_selection_evalutate.errcheck = _check_return_code

    # Function "chfl_selection_matches", at chemfiles.h:943
    c_lib.chfl_selection_matches.argtypes = [POINTER(CHFL_SELECTION), ndpointer(chfl_match_t, flags="C_CONTIGUOUS", ndim=1), c_size_t]
    c_lib.chfl_selection_matches.restype = c_int
    c_lib.chfl_selection_matches.errcheck = _check_return_code

    # Function "chfl_selection_free", at chemfiles.h:952
    c_lib.chfl_selection_free.argtypes = [POINTER(CHFL_SELECTION)]
    c_lib.chfl_selection_free.restype = c_int
    c_lib.chfl_selection_free.errcheck = _check_return_code
