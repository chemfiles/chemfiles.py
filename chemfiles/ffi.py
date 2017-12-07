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
from ctypes import c_int, c_uint64, c_int64, c_double, c_char, c_char_p, c_bool
from ctypes import CFUNCTYPE, ARRAY, POINTER, Structure

from .utils import _check_return_code


class chfl_status(c_int):
    CHFL_SUCCESS = 0
    CHFL_MEMORY_ERROR = 1
    CHFL_FILE_ERROR = 2
    CHFL_FORMAT_ERROR = 3
    CHFL_SELECTION_ERROR = 4
    CHFL_CONFIGURATION_ERROR = 5
    CHFL_OUT_OF_BOUNDS = 6
    CHFL_PROPERTY_ERROR = 7
    CHFL_GENERIC_ERROR = 254
    CHFL_CXX_ERROR = 255


class chfl_property_kind(c_int):
    CHFL_PROPERTY_BOOL = 0
    CHFL_PROPERTY_DOUBLE = 1
    CHFL_PROPERTY_STRING = 2
    CHFL_PROPERTY_VECTOR3D = 3


class chfl_cellshape(c_int):
    CHFL_CELL_ORTHORHOMBIC = 0
    CHFL_CELL_TRICLINIC = 1
    CHFL_CELL_INFINITE = 2


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


class CHFL_RESIDUE(Structure):
    pass


class CHFL_PROPERTY(Structure):
    pass

# Some hand-defined type. Make sure to edit the bindgen code to make this
# correspond to the current chemfiles.h header
chfl_vector3d = ARRAY(c_double, 3)

chfl_warning_callback = CFUNCTYPE(None, c_char_p)

class chfl_match(Structure):
    _fields_ = [
        ('size', c_uint64),
        ('atoms', ARRAY(c_uint64, 4))
    ]

# end of hand-defined types


def set_interface(c_lib):
    from chemfiles import Atom
    from chemfiles import Residue
    from chemfiles import Topology
    from chemfiles import UnitCell
    from chemfiles import Frame
    from chemfiles import Selection
    from chemfiles import Trajectory

    from chemfiles import Property

    # Function "chfl_version", at types.h:145
    c_lib.chfl_version.argtypes = []
    c_lib.chfl_version.restype = c_char_p

    # Function "chfl_last_error", at misc.h:19
    c_lib.chfl_last_error.argtypes = []
    c_lib.chfl_last_error.restype = c_char_p

    # Function "chfl_clear_errors", at misc.h:29
    c_lib.chfl_clear_errors.argtypes = []
    c_lib.chfl_clear_errors.restype = chfl_status
    c_lib.chfl_clear_errors.errcheck = _check_return_code

    # Function "chfl_set_warning_callback", at misc.h:38
    c_lib.chfl_set_warning_callback.argtypes = [chfl_warning_callback]
    c_lib.chfl_set_warning_callback.restype = chfl_status
    c_lib.chfl_set_warning_callback.errcheck = _check_return_code

    # Function "chfl_add_configuration", at misc.h:53
    c_lib.chfl_add_configuration.argtypes = [c_char_p]
    c_lib.chfl_add_configuration.restype = chfl_status
    c_lib.chfl_add_configuration.errcheck = _check_return_code

    # Function "chfl_property_bool", at property.h:32
    c_lib.chfl_property_bool.argtypes = [c_bool]
    c_lib.chfl_property_bool.restype = POINTER(CHFL_PROPERTY)

    # Function "chfl_property_double", at property.h:42
    c_lib.chfl_property_double.argtypes = [c_double]
    c_lib.chfl_property_double.restype = POINTER(CHFL_PROPERTY)

    # Function "chfl_property_string", at property.h:52
    c_lib.chfl_property_string.argtypes = [c_char_p]
    c_lib.chfl_property_string.restype = POINTER(CHFL_PROPERTY)

    # Function "chfl_property_vector3d", at property.h:62
    c_lib.chfl_property_vector3d.argtypes = [chfl_vector3d]
    c_lib.chfl_property_vector3d.restype = POINTER(CHFL_PROPERTY)

    # Function "chfl_property_get_kind", at property.h:69
    c_lib.chfl_property_get_kind.argtypes = [Property, POINTER(chfl_property_kind)]
    c_lib.chfl_property_get_kind.restype = chfl_status
    c_lib.chfl_property_get_kind.errcheck = _check_return_code

    # Function "chfl_property_get_bool", at property.h:82
    c_lib.chfl_property_get_bool.argtypes = [Property, POINTER(c_bool)]
    c_lib.chfl_property_get_bool.restype = chfl_status
    c_lib.chfl_property_get_bool.errcheck = _check_return_code

    # Function "chfl_property_get_double", at property.h:95
    c_lib.chfl_property_get_double.argtypes = [Property, POINTER(c_double)]
    c_lib.chfl_property_get_double.restype = chfl_status
    c_lib.chfl_property_get_double.errcheck = _check_return_code

    # Function "chfl_property_get_string", at property.h:110
    c_lib.chfl_property_get_string.argtypes = [Property, c_char_p, c_uint64]
    c_lib.chfl_property_get_string.restype = chfl_status
    c_lib.chfl_property_get_string.errcheck = _check_return_code

    # Function "chfl_property_get_vector3d", at property.h:123
    c_lib.chfl_property_get_vector3d.argtypes = [Property, chfl_vector3d]
    c_lib.chfl_property_get_vector3d.restype = chfl_status
    c_lib.chfl_property_get_vector3d.errcheck = _check_return_code

    # Function "chfl_property_free", at property.h:131
    c_lib.chfl_property_free.argtypes = [Property]
    c_lib.chfl_property_free.restype = chfl_status
    c_lib.chfl_property_free.errcheck = _check_return_code

    # Function "chfl_atom", at atom.h:20
    c_lib.chfl_atom.argtypes = [c_char_p]
    c_lib.chfl_atom.restype = POINTER(CHFL_ATOM)

    # Function "chfl_atom_copy", at atom.h:30
    c_lib.chfl_atom_copy.argtypes = [Atom]
    c_lib.chfl_atom_copy.restype = POINTER(CHFL_ATOM)

    # Function "chfl_atom_from_frame", at atom.h:42
    c_lib.chfl_atom_from_frame.argtypes = [Frame, c_uint64]
    c_lib.chfl_atom_from_frame.restype = POINTER(CHFL_ATOM)

    # Function "chfl_atom_from_topology", at atom.h:53
    c_lib.chfl_atom_from_topology.argtypes = [Topology, c_uint64]
    c_lib.chfl_atom_from_topology.restype = POINTER(CHFL_ATOM)

    # Function "chfl_atom_mass", at atom.h:64
    c_lib.chfl_atom_mass.argtypes = [Atom, POINTER(c_double)]
    c_lib.chfl_atom_mass.restype = chfl_status
    c_lib.chfl_atom_mass.errcheck = _check_return_code

    # Function "chfl_atom_set_mass", at atom.h:73
    c_lib.chfl_atom_set_mass.argtypes = [Atom, c_double]
    c_lib.chfl_atom_set_mass.restype = chfl_status
    c_lib.chfl_atom_set_mass.errcheck = _check_return_code

    # Function "chfl_atom_charge", at atom.h:82
    c_lib.chfl_atom_charge.argtypes = [Atom, POINTER(c_double)]
    c_lib.chfl_atom_charge.restype = chfl_status
    c_lib.chfl_atom_charge.errcheck = _check_return_code

    # Function "chfl_atom_set_charge", at atom.h:91
    c_lib.chfl_atom_set_charge.argtypes = [Atom, c_double]
    c_lib.chfl_atom_set_charge.restype = chfl_status
    c_lib.chfl_atom_set_charge.errcheck = _check_return_code

    # Function "chfl_atom_type", at atom.h:101
    c_lib.chfl_atom_type.argtypes = [Atom, c_char_p, c_uint64]
    c_lib.chfl_atom_type.restype = chfl_status
    c_lib.chfl_atom_type.errcheck = _check_return_code

    # Function "chfl_atom_set_type", at atom.h:112
    c_lib.chfl_atom_set_type.argtypes = [Atom, c_char_p]
    c_lib.chfl_atom_set_type.restype = chfl_status
    c_lib.chfl_atom_set_type.errcheck = _check_return_code

    # Function "chfl_atom_name", at atom.h:122
    c_lib.chfl_atom_name.argtypes = [Atom, c_char_p, c_uint64]
    c_lib.chfl_atom_name.restype = chfl_status
    c_lib.chfl_atom_name.errcheck = _check_return_code

    # Function "chfl_atom_set_name", at atom.h:133
    c_lib.chfl_atom_set_name.argtypes = [Atom, c_char_p]
    c_lib.chfl_atom_set_name.restype = chfl_status
    c_lib.chfl_atom_set_name.errcheck = _check_return_code

    # Function "chfl_atom_full_name", at atom.h:143
    c_lib.chfl_atom_full_name.argtypes = [Atom, c_char_p, c_uint64]
    c_lib.chfl_atom_full_name.restype = chfl_status
    c_lib.chfl_atom_full_name.errcheck = _check_return_code

    # Function "chfl_atom_vdw_radius", at atom.h:155
    c_lib.chfl_atom_vdw_radius.argtypes = [Atom, POINTER(c_double)]
    c_lib.chfl_atom_vdw_radius.restype = chfl_status
    c_lib.chfl_atom_vdw_radius.errcheck = _check_return_code

    # Function "chfl_atom_covalent_radius", at atom.h:165
    c_lib.chfl_atom_covalent_radius.argtypes = [Atom, POINTER(c_double)]
    c_lib.chfl_atom_covalent_radius.restype = chfl_status
    c_lib.chfl_atom_covalent_radius.errcheck = _check_return_code

    # Function "chfl_atom_atomic_number", at atom.h:175
    c_lib.chfl_atom_atomic_number.argtypes = [Atom, POINTER(c_uint64)]
    c_lib.chfl_atom_atomic_number.restype = chfl_status
    c_lib.chfl_atom_atomic_number.errcheck = _check_return_code

    # Function "chfl_atom_set_property", at atom.h:185
    c_lib.chfl_atom_set_property.argtypes = [Atom, c_char_p, Property]
    c_lib.chfl_atom_set_property.restype = chfl_status
    c_lib.chfl_atom_set_property.errcheck = _check_return_code

    # Function "chfl_atom_get_property", at atom.h:199
    c_lib.chfl_atom_get_property.argtypes = [Atom, c_char_p]
    c_lib.chfl_atom_get_property.restype = POINTER(CHFL_PROPERTY)

    # Function "chfl_atom_free", at atom.h:207
    c_lib.chfl_atom_free.argtypes = [Atom]
    c_lib.chfl_atom_free.restype = chfl_status
    c_lib.chfl_atom_free.errcheck = _check_return_code

    # Function "chfl_residue", at residue.h:20
    c_lib.chfl_residue.argtypes = [c_char_p]
    c_lib.chfl_residue.restype = POINTER(CHFL_RESIDUE)

    # Function "chfl_residue_with_id", at residue.h:30
    c_lib.chfl_residue_with_id.argtypes = [c_char_p, c_uint64]
    c_lib.chfl_residue_with_id.restype = POINTER(CHFL_RESIDUE)

    # Function "chfl_residue_from_topology", at residue.h:46
    c_lib.chfl_residue_from_topology.argtypes = [Topology, c_uint64]
    c_lib.chfl_residue_from_topology.restype = POINTER(CHFL_RESIDUE)

    # Function "chfl_residue_for_atom", at residue.h:62
    c_lib.chfl_residue_for_atom.argtypes = [Topology, c_uint64]
    c_lib.chfl_residue_for_atom.restype = POINTER(CHFL_RESIDUE)

    # Function "chfl_residue_copy", at residue.h:74
    c_lib.chfl_residue_copy.argtypes = [Residue]
    c_lib.chfl_residue_copy.restype = POINTER(CHFL_RESIDUE)

    # Function "chfl_residue_atoms_count", at residue.h:81
    c_lib.chfl_residue_atoms_count.argtypes = [Residue, POINTER(c_uint64)]
    c_lib.chfl_residue_atoms_count.restype = chfl_status
    c_lib.chfl_residue_atoms_count.errcheck = _check_return_code

    # Function "chfl_residue_atoms", at residue.h:95
    c_lib.chfl_residue_atoms.argtypes = [Residue, ndpointer(np.uint64, flags="C_CONTIGUOUS", ndim=1), c_uint64]
    c_lib.chfl_residue_atoms.restype = chfl_status
    c_lib.chfl_residue_atoms.errcheck = _check_return_code

    # Function "chfl_residue_id", at residue.h:108
    c_lib.chfl_residue_id.argtypes = [Residue, POINTER(c_uint64)]
    c_lib.chfl_residue_id.restype = chfl_status
    c_lib.chfl_residue_id.errcheck = _check_return_code

    # Function "chfl_residue_name", at residue.h:120
    c_lib.chfl_residue_name.argtypes = [Residue, c_char_p, c_uint64]
    c_lib.chfl_residue_name.restype = chfl_status
    c_lib.chfl_residue_name.errcheck = _check_return_code

    # Function "chfl_residue_add_atom", at residue.h:129
    c_lib.chfl_residue_add_atom.argtypes = [Residue, c_uint64]
    c_lib.chfl_residue_add_atom.restype = chfl_status
    c_lib.chfl_residue_add_atom.errcheck = _check_return_code

    # Function "chfl_residue_contains", at residue.h:139
    c_lib.chfl_residue_contains.argtypes = [Residue, c_uint64, POINTER(c_bool)]
    c_lib.chfl_residue_contains.restype = chfl_status
    c_lib.chfl_residue_contains.errcheck = _check_return_code

    # Function "chfl_residue_free", at residue.h:147
    c_lib.chfl_residue_free.argtypes = [Residue]
    c_lib.chfl_residue_free.restype = chfl_status
    c_lib.chfl_residue_free.errcheck = _check_return_code

    # Function "chfl_topology", at topology.h:20
    c_lib.chfl_topology.argtypes = []
    c_lib.chfl_topology.restype = POINTER(CHFL_TOPOLOGY)

    # Function "chfl_topology_from_frame", at topology.h:30
    c_lib.chfl_topology_from_frame.argtypes = [Frame]
    c_lib.chfl_topology_from_frame.restype = POINTER(CHFL_TOPOLOGY)

    # Function "chfl_topology_copy", at topology.h:40
    c_lib.chfl_topology_copy.argtypes = [Topology]
    c_lib.chfl_topology_copy.restype = POINTER(CHFL_TOPOLOGY)

    # Function "chfl_topology_atoms_count", at topology.h:48
    c_lib.chfl_topology_atoms_count.argtypes = [Topology, POINTER(c_uint64)]
    c_lib.chfl_topology_atoms_count.restype = chfl_status
    c_lib.chfl_topology_atoms_count.errcheck = _check_return_code

    # Function "chfl_topology_resize", at topology.h:60
    c_lib.chfl_topology_resize.argtypes = [Topology, c_uint64]
    c_lib.chfl_topology_resize.restype = chfl_status
    c_lib.chfl_topology_resize.errcheck = _check_return_code

    # Function "chfl_topology_add_atom", at topology.h:67
    c_lib.chfl_topology_add_atom.argtypes = [Topology, Atom]
    c_lib.chfl_topology_add_atom.restype = chfl_status
    c_lib.chfl_topology_add_atom.errcheck = _check_return_code

    # Function "chfl_topology_remove", at topology.h:78
    c_lib.chfl_topology_remove.argtypes = [Topology, c_uint64]
    c_lib.chfl_topology_remove.restype = chfl_status
    c_lib.chfl_topology_remove.errcheck = _check_return_code

    # Function "chfl_topology_bonds_count", at topology.h:87
    c_lib.chfl_topology_bonds_count.argtypes = [Topology, POINTER(c_uint64)]
    c_lib.chfl_topology_bonds_count.restype = chfl_status
    c_lib.chfl_topology_bonds_count.errcheck = _check_return_code

    # Function "chfl_topology_angles_count", at topology.h:96
    c_lib.chfl_topology_angles_count.argtypes = [Topology, POINTER(c_uint64)]
    c_lib.chfl_topology_angles_count.restype = chfl_status
    c_lib.chfl_topology_angles_count.errcheck = _check_return_code

    # Function "chfl_topology_dihedrals_count", at topology.h:105
    c_lib.chfl_topology_dihedrals_count.argtypes = [Topology, POINTER(c_uint64)]
    c_lib.chfl_topology_dihedrals_count.restype = chfl_status
    c_lib.chfl_topology_dihedrals_count.errcheck = _check_return_code

    # Function "chfl_topology_impropers_count", at topology.h:114
    c_lib.chfl_topology_impropers_count.argtypes = [Topology, POINTER(c_uint64)]
    c_lib.chfl_topology_impropers_count.restype = chfl_status
    c_lib.chfl_topology_impropers_count.errcheck = _check_return_code

    # Function "chfl_topology_bonds", at topology.h:127
    c_lib.chfl_topology_bonds.argtypes = [Topology, ndpointer(np.uint64, flags="C_CONTIGUOUS", ndim=2), c_uint64]
    c_lib.chfl_topology_bonds.restype = chfl_status
    c_lib.chfl_topology_bonds.errcheck = _check_return_code

    # Function "chfl_topology_angles", at topology.h:140
    c_lib.chfl_topology_angles.argtypes = [Topology, ndpointer(np.uint64, flags="C_CONTIGUOUS", ndim=2), c_uint64]
    c_lib.chfl_topology_angles.restype = chfl_status
    c_lib.chfl_topology_angles.errcheck = _check_return_code

    # Function "chfl_topology_dihedrals", at topology.h:154
    c_lib.chfl_topology_dihedrals.argtypes = [Topology, ndpointer(np.uint64, flags="C_CONTIGUOUS", ndim=2), c_uint64]
    c_lib.chfl_topology_dihedrals.restype = chfl_status
    c_lib.chfl_topology_dihedrals.errcheck = _check_return_code

    # Function "chfl_topology_impropers", at topology.h:168
    c_lib.chfl_topology_impropers.argtypes = [Topology, ndpointer(np.uint64, flags="C_CONTIGUOUS", ndim=2), c_uint64]
    c_lib.chfl_topology_impropers.restype = chfl_status
    c_lib.chfl_topology_impropers.errcheck = _check_return_code

    # Function "chfl_topology_add_bond", at topology.h:177
    c_lib.chfl_topology_add_bond.argtypes = [Topology, c_uint64, c_uint64]
    c_lib.chfl_topology_add_bond.restype = chfl_status
    c_lib.chfl_topology_add_bond.errcheck = _check_return_code

    # Function "chfl_topology_remove_bond", at topology.h:189
    c_lib.chfl_topology_remove_bond.argtypes = [Topology, c_uint64, c_uint64]
    c_lib.chfl_topology_remove_bond.restype = chfl_status
    c_lib.chfl_topology_remove_bond.errcheck = _check_return_code

    # Function "chfl_topology_residues_count", at topology.h:199
    c_lib.chfl_topology_residues_count.argtypes = [Topology, POINTER(c_uint64)]
    c_lib.chfl_topology_residues_count.restype = chfl_status
    c_lib.chfl_topology_residues_count.errcheck = _check_return_code

    # Function "chfl_topology_add_residue", at topology.h:211
    c_lib.chfl_topology_add_residue.argtypes = [Topology, Residue]
    c_lib.chfl_topology_add_residue.restype = chfl_status
    c_lib.chfl_topology_add_residue.errcheck = _check_return_code

    # Function "chfl_topology_residues_linked", at topology.h:222
    c_lib.chfl_topology_residues_linked.argtypes = [Topology, Residue, Residue, POINTER(c_bool)]
    c_lib.chfl_topology_residues_linked.restype = chfl_status
    c_lib.chfl_topology_residues_linked.errcheck = _check_return_code

    # Function "chfl_topology_free", at topology.h:233
    c_lib.chfl_topology_free.argtypes = [Topology]
    c_lib.chfl_topology_free.restype = chfl_status
    c_lib.chfl_topology_free.errcheck = _check_return_code

    # Function "chfl_cell", at cell.h:33
    c_lib.chfl_cell.argtypes = [chfl_vector3d]
    c_lib.chfl_cell.restype = POINTER(CHFL_CELL)

    # Function "chfl_cell_triclinic", at cell.h:50
    c_lib.chfl_cell_triclinic.argtypes = [chfl_vector3d, chfl_vector3d]
    c_lib.chfl_cell_triclinic.restype = POINTER(CHFL_CELL)

    # Function "chfl_cell_from_frame", at cell.h:62
    c_lib.chfl_cell_from_frame.argtypes = [Frame]
    c_lib.chfl_cell_from_frame.restype = POINTER(CHFL_CELL)

    # Function "chfl_cell_copy", at cell.h:72
    c_lib.chfl_cell_copy.argtypes = [UnitCell]
    c_lib.chfl_cell_copy.restype = POINTER(CHFL_CELL)

    # Function "chfl_cell_volume", at cell.h:79
    c_lib.chfl_cell_volume.argtypes = [UnitCell, POINTER(c_double)]
    c_lib.chfl_cell_volume.restype = chfl_status
    c_lib.chfl_cell_volume.errcheck = _check_return_code

    # Function "chfl_cell_lengths", at cell.h:88
    c_lib.chfl_cell_lengths.argtypes = [UnitCell, chfl_vector3d]
    c_lib.chfl_cell_lengths.restype = chfl_status
    c_lib.chfl_cell_lengths.errcheck = _check_return_code

    # Function "chfl_cell_set_lengths", at cell.h:99
    c_lib.chfl_cell_set_lengths.argtypes = [UnitCell, chfl_vector3d]
    c_lib.chfl_cell_set_lengths.restype = chfl_status
    c_lib.chfl_cell_set_lengths.errcheck = _check_return_code

    # Function "chfl_cell_angles", at cell.h:108
    c_lib.chfl_cell_angles.argtypes = [UnitCell, chfl_vector3d]
    c_lib.chfl_cell_angles.restype = chfl_status
    c_lib.chfl_cell_angles.errcheck = _check_return_code

    # Function "chfl_cell_set_angles", at cell.h:121
    c_lib.chfl_cell_set_angles.argtypes = [UnitCell, chfl_vector3d]
    c_lib.chfl_cell_set_angles.restype = chfl_status
    c_lib.chfl_cell_set_angles.errcheck = _check_return_code

    # Function "chfl_cell_matrix", at cell.h:139
    c_lib.chfl_cell_matrix.argtypes = [UnitCell, ARRAY(chfl_vector3d, (3))]
    c_lib.chfl_cell_matrix.restype = chfl_status
    c_lib.chfl_cell_matrix.errcheck = _check_return_code

    # Function "chfl_cell_shape", at cell.h:148
    c_lib.chfl_cell_shape.argtypes = [UnitCell, POINTER(chfl_cellshape)]
    c_lib.chfl_cell_shape.restype = chfl_status
    c_lib.chfl_cell_shape.errcheck = _check_return_code

    # Function "chfl_cell_set_shape", at cell.h:157
    c_lib.chfl_cell_set_shape.argtypes = [UnitCell, chfl_cellshape]
    c_lib.chfl_cell_set_shape.restype = chfl_status
    c_lib.chfl_cell_set_shape.errcheck = _check_return_code

    # Function "chfl_cell_wrap", at cell.h:166
    c_lib.chfl_cell_wrap.argtypes = [UnitCell, chfl_vector3d]
    c_lib.chfl_cell_wrap.restype = chfl_status
    c_lib.chfl_cell_wrap.errcheck = _check_return_code

    # Function "chfl_cell_free", at cell.h:174
    c_lib.chfl_cell_free.argtypes = [UnitCell]
    c_lib.chfl_cell_free.restype = chfl_status
    c_lib.chfl_cell_free.errcheck = _check_return_code

    # Function "chfl_frame", at frame.h:20
    c_lib.chfl_frame.argtypes = []
    c_lib.chfl_frame.restype = POINTER(CHFL_FRAME)

    # Function "chfl_frame_copy", at frame.h:30
    c_lib.chfl_frame_copy.argtypes = [Frame]
    c_lib.chfl_frame_copy.restype = POINTER(CHFL_FRAME)

    # Function "chfl_frame_atoms_count", at frame.h:38
    c_lib.chfl_frame_atoms_count.argtypes = [Frame, POINTER(c_uint64)]
    c_lib.chfl_frame_atoms_count.restype = chfl_status
    c_lib.chfl_frame_atoms_count.errcheck = _check_return_code

    # Function "chfl_frame_positions", at frame.h:57
    c_lib.chfl_frame_positions.argtypes = [Frame, POINTER(POINTER(chfl_vector3d)), POINTER(c_uint64)]
    c_lib.chfl_frame_positions.restype = chfl_status
    c_lib.chfl_frame_positions.errcheck = _check_return_code

    # Function "chfl_frame_velocities", at frame.h:80
    c_lib.chfl_frame_velocities.argtypes = [Frame, POINTER(POINTER(chfl_vector3d)), POINTER(c_uint64)]
    c_lib.chfl_frame_velocities.restype = chfl_status
    c_lib.chfl_frame_velocities.errcheck = _check_return_code

    # Function "chfl_frame_add_atom", at frame.h:92
    c_lib.chfl_frame_add_atom.argtypes = [Frame, Atom, chfl_vector3d, chfl_vector3d]
    c_lib.chfl_frame_add_atom.restype = chfl_status
    c_lib.chfl_frame_add_atom.errcheck = _check_return_code

    # Function "chfl_frame_remove", at frame.h:105
    c_lib.chfl_frame_remove.argtypes = [Frame, c_uint64]
    c_lib.chfl_frame_remove.restype = chfl_status
    c_lib.chfl_frame_remove.errcheck = _check_return_code

    # Function "chfl_frame_resize", at frame.h:117
    c_lib.chfl_frame_resize.argtypes = [Frame, c_uint64]
    c_lib.chfl_frame_resize.restype = chfl_status
    c_lib.chfl_frame_resize.errcheck = _check_return_code

    # Function "chfl_frame_add_velocities", at frame.h:129
    c_lib.chfl_frame_add_velocities.argtypes = [Frame]
    c_lib.chfl_frame_add_velocities.restype = chfl_status
    c_lib.chfl_frame_add_velocities.errcheck = _check_return_code

    # Function "chfl_frame_has_velocities", at frame.h:137
    c_lib.chfl_frame_has_velocities.argtypes = [Frame, POINTER(c_bool)]
    c_lib.chfl_frame_has_velocities.restype = chfl_status
    c_lib.chfl_frame_has_velocities.errcheck = _check_return_code

    # Function "chfl_frame_set_cell", at frame.h:146
    c_lib.chfl_frame_set_cell.argtypes = [Frame, UnitCell]
    c_lib.chfl_frame_set_cell.restype = chfl_status
    c_lib.chfl_frame_set_cell.errcheck = _check_return_code

    # Function "chfl_frame_set_topology", at frame.h:158
    c_lib.chfl_frame_set_topology.argtypes = [Frame, Topology]
    c_lib.chfl_frame_set_topology.restype = chfl_status
    c_lib.chfl_frame_set_topology.errcheck = _check_return_code

    # Function "chfl_frame_step", at frame.h:168
    c_lib.chfl_frame_step.argtypes = [Frame, POINTER(c_uint64)]
    c_lib.chfl_frame_step.restype = chfl_status
    c_lib.chfl_frame_step.errcheck = _check_return_code

    # Function "chfl_frame_set_step", at frame.h:177
    c_lib.chfl_frame_set_step.argtypes = [Frame, c_uint64]
    c_lib.chfl_frame_set_step.restype = chfl_status
    c_lib.chfl_frame_set_step.errcheck = _check_return_code

    # Function "chfl_frame_guess_topology", at frame.h:189
    c_lib.chfl_frame_guess_topology.argtypes = [Frame]
    c_lib.chfl_frame_guess_topology.restype = chfl_status
    c_lib.chfl_frame_guess_topology.errcheck = _check_return_code

    # Function "chfl_frame_distance", at frame.h:198
    c_lib.chfl_frame_distance.argtypes = [Frame, c_uint64, c_uint64, POINTER(c_double)]
    c_lib.chfl_frame_distance.restype = chfl_status
    c_lib.chfl_frame_distance.errcheck = _check_return_code

    # Function "chfl_frame_angle", at frame.h:209
    c_lib.chfl_frame_angle.argtypes = [Frame, c_uint64, c_uint64, c_uint64, POINTER(c_double)]
    c_lib.chfl_frame_angle.restype = chfl_status
    c_lib.chfl_frame_angle.errcheck = _check_return_code

    # Function "chfl_frame_dihedral", at frame.h:220
    c_lib.chfl_frame_dihedral.argtypes = [Frame, c_uint64, c_uint64, c_uint64, c_uint64, POINTER(c_double)]
    c_lib.chfl_frame_dihedral.restype = chfl_status
    c_lib.chfl_frame_dihedral.errcheck = _check_return_code

    # Function "chfl_frame_out_of_plane", at frame.h:234
    c_lib.chfl_frame_out_of_plane.argtypes = [Frame, c_uint64, c_uint64, c_uint64, c_uint64, POINTER(c_double)]
    c_lib.chfl_frame_out_of_plane.restype = chfl_status
    c_lib.chfl_frame_out_of_plane.errcheck = _check_return_code

    # Function "chfl_frame_set_property", at frame.h:246
    c_lib.chfl_frame_set_property.argtypes = [Frame, c_char_p, Property]
    c_lib.chfl_frame_set_property.restype = chfl_status
    c_lib.chfl_frame_set_property.errcheck = _check_return_code

    # Function "chfl_frame_get_property", at frame.h:260
    c_lib.chfl_frame_get_property.argtypes = [Frame, c_char_p]
    c_lib.chfl_frame_get_property.restype = POINTER(CHFL_PROPERTY)

    # Function "chfl_frame_add_bond", at frame.h:269
    c_lib.chfl_frame_add_bond.argtypes = [Frame, c_uint64, c_uint64]
    c_lib.chfl_frame_add_bond.restype = chfl_status
    c_lib.chfl_frame_add_bond.errcheck = _check_return_code

    # Function "chfl_frame_remove_bond", at frame.h:281
    c_lib.chfl_frame_remove_bond.argtypes = [Frame, c_uint64, c_uint64]
    c_lib.chfl_frame_remove_bond.restype = chfl_status
    c_lib.chfl_frame_remove_bond.errcheck = _check_return_code

    # Function "chfl_frame_add_residue", at frame.h:293
    c_lib.chfl_frame_add_residue.argtypes = [Frame, Residue]
    c_lib.chfl_frame_add_residue.restype = chfl_status
    c_lib.chfl_frame_add_residue.errcheck = _check_return_code

    # Function "chfl_frame_free", at frame.h:301
    c_lib.chfl_frame_free.argtypes = [Frame]
    c_lib.chfl_frame_free.restype = chfl_status
    c_lib.chfl_frame_free.errcheck = _check_return_code

    # Function "chfl_trajectory_open", at trajectory.h:22
    c_lib.chfl_trajectory_open.argtypes = [c_char_p, c_char]
    c_lib.chfl_trajectory_open.restype = POINTER(CHFL_TRAJECTORY)

    # Function "chfl_trajectory_with_format", at trajectory.h:39
    c_lib.chfl_trajectory_with_format.argtypes = [c_char_p, c_char, c_char_p]
    c_lib.chfl_trajectory_with_format.restype = POINTER(CHFL_TRAJECTORY)

    # Function "chfl_trajectory_read", at trajectory.h:51
    c_lib.chfl_trajectory_read.argtypes = [Trajectory, Frame]
    c_lib.chfl_trajectory_read.restype = chfl_status
    c_lib.chfl_trajectory_read.errcheck = _check_return_code

    # Function "chfl_trajectory_read_step", at trajectory.h:63
    c_lib.chfl_trajectory_read_step.argtypes = [Trajectory, c_uint64, Frame]
    c_lib.chfl_trajectory_read_step.restype = chfl_status
    c_lib.chfl_trajectory_read_step.errcheck = _check_return_code

    # Function "chfl_trajectory_write", at trajectory.h:72
    c_lib.chfl_trajectory_write.argtypes = [Trajectory, Frame]
    c_lib.chfl_trajectory_write.restype = chfl_status
    c_lib.chfl_trajectory_write.errcheck = _check_return_code

    # Function "chfl_trajectory_set_topology", at trajectory.h:83
    c_lib.chfl_trajectory_set_topology.argtypes = [Trajectory, Topology]
    c_lib.chfl_trajectory_set_topology.restype = chfl_status
    c_lib.chfl_trajectory_set_topology.errcheck = _check_return_code

    # Function "chfl_trajectory_topology_file", at trajectory.h:97
    c_lib.chfl_trajectory_topology_file.argtypes = [Trajectory, c_char_p, c_char_p]
    c_lib.chfl_trajectory_topology_file.restype = chfl_status
    c_lib.chfl_trajectory_topology_file.errcheck = _check_return_code

    # Function "chfl_trajectory_set_cell", at trajectory.h:107
    c_lib.chfl_trajectory_set_cell.argtypes = [Trajectory, UnitCell]
    c_lib.chfl_trajectory_set_cell.restype = chfl_status
    c_lib.chfl_trajectory_set_cell.errcheck = _check_return_code

    # Function "chfl_trajectory_nsteps", at trajectory.h:117
    c_lib.chfl_trajectory_nsteps.argtypes = [Trajectory, POINTER(c_uint64)]
    c_lib.chfl_trajectory_nsteps.restype = chfl_status
    c_lib.chfl_trajectory_nsteps.errcheck = _check_return_code

    # Function "chfl_trajectory_close", at trajectory.h:128
    c_lib.chfl_trajectory_close.argtypes = [Trajectory]
    c_lib.chfl_trajectory_close.restype = chfl_status
    c_lib.chfl_trajectory_close.errcheck = _check_return_code

    # Function "chfl_selection", at selection.h:20
    c_lib.chfl_selection.argtypes = [c_char_p]
    c_lib.chfl_selection.restype = POINTER(CHFL_SELECTION)

    # Function "chfl_selection_copy", at selection.h:33
    c_lib.chfl_selection_copy.argtypes = [Selection]
    c_lib.chfl_selection_copy.restype = POINTER(CHFL_SELECTION)

    # Function "chfl_selection_size", at selection.h:45
    c_lib.chfl_selection_size.argtypes = [Selection, POINTER(c_uint64)]
    c_lib.chfl_selection_size.restype = chfl_status
    c_lib.chfl_selection_size.errcheck = _check_return_code

    # Function "chfl_selection_string", at selection.h:58
    c_lib.chfl_selection_string.argtypes = [Selection, c_char_p, c_uint64]
    c_lib.chfl_selection_string.restype = chfl_status
    c_lib.chfl_selection_string.errcheck = _check_return_code

    # Function "chfl_selection_evaluate", at selection.h:71
    c_lib.chfl_selection_evaluate.argtypes = [Selection, Frame, POINTER(c_uint64)]
    c_lib.chfl_selection_evaluate.restype = chfl_status
    c_lib.chfl_selection_evaluate.errcheck = _check_return_code

    # Function "chfl_selection_matches", at selection.h:97
    c_lib.chfl_selection_matches.argtypes = [Selection, ndpointer(chfl_match, flags="C_CONTIGUOUS", ndim=1), c_uint64]
    c_lib.chfl_selection_matches.restype = chfl_status
    c_lib.chfl_selection_matches.errcheck = _check_return_code

    # Function "chfl_selection_free", at selection.h:105
    c_lib.chfl_selection_free.argtypes = [Selection]
    c_lib.chfl_selection_free.restype = chfl_status
    c_lib.chfl_selection_free.errcheck = _check_return_code
