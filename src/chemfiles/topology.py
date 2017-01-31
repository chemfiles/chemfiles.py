# -*- coding=utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals
from ctypes import c_uint64, c_bool, byref
import numpy as np

from chemfiles import get_c_library
from chemfiles.errors import _check_handle, NullPointerError
from chemfiles import Atom, Residue


class Topology(object):
    '''
    A :py:class:`Topology` contains the definition of all the particles in the
    system, and the liaisons between the particles (bonds, angles, dihedrals,
    ...).

    Only the atoms and the bonds are stored, the angles and the dihedrals are
    computed automaticaly.
    '''

    def __init__(self):
        '''Create a new empty :py:class:`Topology`.'''
        self.c_lib = get_c_library()
        self._handle_ = self.c_lib.chfl_topology()
        _check_handle(self._handle_)

    def __del__(self):
        self.c_lib.chfl_topology_free(self._handle_)

    def __copy__(self):
        topology = self.__new__(Topology)
        topology.c_lib = get_c_library()
        topology._handle_ = self.c_lib.chfl_topology_copy(self._handle_)
        _check_handle(topology._handle_)
        return topology

    def atom(self, index):
        '''
        Get the :py:class:`Atom` at ``index`` from a :py:class:`Topology`.
        '''
        atom = Atom("")
        self.c_lib.chfl_atom_free(atom._handle_)
        atom._handle_ = self.c_lib.chfl_atom_from_topology(
            self._handle_, c_uint64(index)
        )
        try:
            _check_handle(atom._handle_)
        except NullPointerError:
            raise IndexError("No atom at index {} in frame".format(index))
        return atom

    def natoms(self):
        '''Get the current number of atoms in the :py:class:`Topology`.'''
        res = c_uint64()
        self.c_lib.chfl_topology_atoms_count(self._handle_, res)
        return res.value

    def __len__(self):
        '''Get the current number of atoms in the :py:class:`Topology`.'''
        return self.natoms()

    def resize(self, natoms):
        '''
        Resize the :py:class:`Topology` to contain ``natoms`` atoms. If the new
        number of atoms is bigger than the current number, new atoms will be
        created with an empty name and type.
        '''
        self.c_lib.chfl_topology_resize(self._handle_, natoms)

    def add_atom(self, atom):
        '''Add an :py:class:`Atom` at the end of the :py:class:`Topology`'''
        self.c_lib.chfl_topology_add_atom(self._handle_, atom._handle_)

    def remove(self, index):
        '''
        Remove an :py:class:`Atom` from the :py:class:`Topology` by index. This
        can modify all the other atoms indexes.
        '''
        self.c_lib.chfl_topology_remove(self._handle_, c_uint64(index))

    def residue(self, index):
        '''
        Get the :py:class:`Residue` at ``index`` from the :py:class:`Topology`.
        '''
        residue = Residue("")
        self.c_lib.chfl_residue_free(residue._handle_)
        residue._handle_ = self.c_lib.chfl_residue_from_topology(
            self._handle_, c_uint64(index)
        )
        try:
            _check_handle(residue._handle_)
        except NullPointerError:
            raise IndexError("No residue at index {} in frame".format(index))
        return residue

    def residue_for_atom(self, index):
        '''
        Get the :py:class:`Residue` containing the atom at ``index`` from the
        :py:class:`Topology`. If the atom is not in a residue, this function
        returns None.
        '''
        residue = Residue("")
        self.c_lib.chfl_residue_free(residue._handle_)
        residue._handle_ = self.c_lib.chfl_residue_for_atom(
            self._handle_, c_uint64(index)
        )
        try:
            _check_handle(residue._handle_)
            return residue
        except NullPointerError:
            return None

    def residues_count(self):
        '''Get the current number of residues in the :py:class:`Topology`.'''
        res = c_uint64()
        self.c_lib.chfl_topology_residues_count(self._handle_, res)
        return res.value

    def add_residue(self, residue):
        '''Add a :py:class:`Residue` to this :py:class:`Topology`.'''
        self.c_lib.chfl_topology_add_residue(self._handle_, residue._handle_)

    def residues_linked(self, first, second):
        '''
        Check if the two :py:class:`Residue` ``first`` and ``second`` from the
        :py:class:`Topology` are linked together, *i.e.* if there is a bond
        between one atom in the first residue and one atom in the second one.
        '''
        res = c_bool()
        self.c_lib.chfl_topology_residues_linked(
            self._handle_, first._handle_, second._handle_, res
        )
        return res.value

    def isbond(self, i, j):
        '''Tell if the atoms at indexes ``i`` and ``j`` are bonded together'''
        res = c_bool()
        self.c_lib.chfl_topology_isbond(
            self._handle_, c_uint64(i), c_uint64(j), byref(res)
        )
        return res.value

    def isangle(self, i, j, k):
        '''
        Tell if the atoms at indexes ``i``, ``j`` and ``k`` constitues an angle
        '''
        res = c_bool()
        self.c_lib.chfl_topology_isangle(
            self._handle_, c_uint64(i), c_uint64(j), c_uint64(k), byref(res)
        )
        return res.value

    def isdihedral(self, i, j, k, m):
        '''
        Tell if the atoms at indexes ``i``, ``j``, ``k`` and ``m`` constitues a
        dihedral angle
        '''
        res = c_bool()
        self.c_lib.chfl_topology_isdihedral(
            self._handle_,
            c_uint64(i), c_uint64(j), c_uint64(k), c_uint64(m),
            byref(res)
        )
        return res.value

    def bonds_count(self):
        '''Get the number of bonds in the system'''
        res = c_uint64()
        self.c_lib.chfl_topology_bonds_count(self._handle_, byref(res))
        return res.value

    def angles_count(self):
        '''Get the number of angles in the system'''
        res = c_uint64()
        self.c_lib.chfl_topology_angles_count(self._handle_, byref(res))
        return res.value

    def dihedrals_count(self):
        '''Get the number of dihedral angles in the system'''
        res = c_uint64()
        self.c_lib.chfl_topology_dihedrals_count(self._handle_, byref(res))
        return res.value

    def bonds(self):
        '''Get the list of bonds in the system'''
        nbonds = self.bonds_count()
        res = np.zeros((nbonds, 2), np.uintp)
        self.c_lib.chfl_topology_bonds(self._handle_, res, c_uint64(nbonds))
        return res

    def angles(self):
        '''Get the list of angles in the system'''
        nangles = self.angles_count()
        res = np.zeros((nangles, 3), np.uintp)
        self.c_lib.chfl_topology_angles(self._handle_, res, c_uint64(nangles))
        return res

    def dihedrals(self):
        '''Get the list of dihedral angles in the system'''
        ndihedrals = self.dihedrals_count()
        res = np.zeros((ndihedrals, 4), np.uintp)
        self.c_lib.chfl_topology_dihedrals(
            self._handle_, res, c_uint64(ndihedrals)
        )
        return res

    def add_bond(self, i, j):
        '''
        Add a bond between the atoms at indexes ``i`` and ``j`` in the system
        '''
        self.c_lib.chfl_topology_add_bond(
            self._handle_, c_uint64(i), c_uint64(j)
        )

    def remove_bond(self, i, j):
        '''
        Remove any existing bond between the atoms at indexes ``i`` and ``j``
        in the system
        '''
        self.c_lib.chfl_topology_remove_bond(
            self._handle_, c_uint64(i), c_uint64(j)
        )
