# -*- coding=utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals
from ctypes import c_uint64, c_bool, byref
import numpy as np

from chemfiles.types import CxxPointer
from chemfiles import Atom, Residue


class Topology(CxxPointer):
    '''
    A :py:class:`Topology` contains the definition of all the particles in the
    system, and the liaisons between the particles (bonds, angles, dihedrals,
    ...).

    Only the atoms and the bonds are stored, the angles and the dihedrals are
    computed automaticaly.
    '''

    def __init__(self):
        '''Create a new empty :py:class:`Topology`.'''
        super(Topology, self).__init__(self.ffi.chfl_topology())

    def __del__(self):
        self.ffi.chfl_topology_free(self)

    def __copy__(self):
        return Topology.from_ptr(self.ffi.chfl_topology_copy(self))

    def atom(self, index):
        '''
        Get the :py:class:`Atom` at ``index`` from a :py:class:`Topology`.
        '''
        ptr = self.ffi.chfl_atom_from_topology(self, c_uint64(index))
        if not ptr:
            raise IndexError("No atom at index {} in frame".format(index))
        return Atom.from_ptr(ptr)

    def natoms(self):
        '''Get the current number of atoms in the :py:class:`Topology`.'''
        res = c_uint64()
        self.ffi.chfl_topology_atoms_count(self, res)
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
        self.ffi.chfl_topology_resize(self, natoms)

    def add_atom(self, atom):
        '''Add an :py:class:`Atom` at the end of the :py:class:`Topology`'''
        self.ffi.chfl_topology_add_atom(self, atom)

    def remove(self, index):
        '''
        Remove an :py:class:`Atom` from the :py:class:`Topology` by index. This
        can modify all the other atoms indexes.
        '''
        self.ffi.chfl_topology_remove(self, c_uint64(index))

    def residue(self, index):
        '''
        Get the :py:class:`Residue` at ``index`` from the :py:class:`Topology`.
        '''
        ptr = self.ffi.chfl_residue_from_topology(self, c_uint64(index))
        if not ptr:
            raise IndexError("No residue at index {} in frame".format(index))
        return Residue.from_ptr(ptr)

    def residue_for_atom(self, index):
        '''
        Get the :py:class:`Residue` containing the atom at ``index`` from the
        :py:class:`Topology`. If the atom is not in a residue, this function
        returns None.
        '''
        ptr = self.ffi.chfl_residue_for_atom(self, c_uint64(index))
        if ptr:
            return Residue.from_ptr(ptr)
        else:
            return None

    def residues_count(self):
        '''Get the current number of residues in the :py:class:`Topology`.'''
        res = c_uint64()
        self.ffi.chfl_topology_residues_count(self, res)
        return res.value

    def add_residue(self, residue):
        '''Add a :py:class:`Residue` to this :py:class:`Topology`.'''
        self.ffi.chfl_topology_add_residue(self, residue)

    def residues_linked(self, first, second):
        '''
        Check if the two :py:class:`Residue` ``first`` and ``second`` from the
        :py:class:`Topology` are linked together, *i.e.* if there is a bond
        between one atom in the first residue and one atom in the second one.
        '''
        res = c_bool()
        self.ffi.chfl_topology_residues_linked(self, first, second, res)
        return res.value

    def isbond(self, i, j):
        '''Tell if the atoms at indexes ``i`` and ``j`` are bonded together'''
        res = c_bool()
        self.ffi.chfl_topology_isbond(
            self, c_uint64(i), c_uint64(j), res
        )
        return res.value

    def isangle(self, i, j, k):
        '''
        Tell if the atoms at indexes ``i``, ``j`` and ``k`` constitues an angle
        '''
        res = c_bool()
        self.ffi.chfl_topology_isangle(
            self, c_uint64(i), c_uint64(j), c_uint64(k), res
        )
        return res.value

    def isdihedral(self, i, j, k, m):
        '''
        Tell if the atoms at indexes ``i``, ``j``, ``k`` and ``m`` constitues a
        dihedral angle
        '''
        res = c_bool()
        self.ffi.chfl_topology_isdihedral(
            self, c_uint64(i), c_uint64(j), c_uint64(k), c_uint64(m), res
        )
        return res.value

    def bonds_count(self):
        '''Get the number of bonds in the system'''
        res = c_uint64()
        self.ffi.chfl_topology_bonds_count(self, byref(res))
        return res.value

    def angles_count(self):
        '''Get the number of angles in the system'''
        res = c_uint64()
        self.ffi.chfl_topology_angles_count(self, byref(res))
        return res.value

    def dihedrals_count(self):
        '''Get the number of dihedral angles in the system'''
        res = c_uint64()
        self.ffi.chfl_topology_dihedrals_count(self, byref(res))
        return res.value

    def bonds(self):
        '''Get the list of bonds in the system'''
        nbonds = self.bonds_count()
        res = np.zeros((nbonds, 2), np.uintp)
        self.ffi.chfl_topology_bonds(self, res, c_uint64(nbonds))
        return res

    def angles(self):
        '''Get the list of angles in the system'''
        nangles = self.angles_count()
        res = np.zeros((nangles, 3), np.uintp)
        self.ffi.chfl_topology_angles(self, res, c_uint64(nangles))
        return res

    def dihedrals(self):
        '''Get the list of dihedral angles in the system'''
        ndihedrals = self.dihedrals_count()
        res = np.zeros((ndihedrals, 4), np.uintp)
        self.ffi.chfl_topology_dihedrals(self, res, c_uint64(ndihedrals))
        return res

    def add_bond(self, i, j):
        '''
        Add a bond between the atoms at indexes ``i`` and ``j`` in the system
        '''
        self.ffi.chfl_topology_add_bond(self, c_uint64(i), c_uint64(j))

    def remove_bond(self, i, j):
        '''
        Remove any existing bond between the atoms at indexes ``i`` and ``j``
        in the system
        '''
        self.ffi.chfl_topology_remove_bond(self, c_uint64(i), c_uint64(j))
