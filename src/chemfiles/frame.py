# -*- coding=utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals
import numpy as np
from ctypes import c_uint64, c_bool, byref, POINTER

from chemfiles.ffi import chfl_vector_t
from chemfiles.types import CxxPointer
from chemfiles import Atom, Topology, UnitCell


class Frame(CxxPointer):
    '''
    A :py:class:`Frame` holds data from one step of a simulation: the current
    :py:class:`Topology`, the positions, and maybe the velocities of the
    particles in the system.
    '''

    def __init__(self, natoms=0):
        '''
        Create an empty frame with initial capacity of `natoms`. It will be
        resized by the library as needed.
        '''
        super(Frame, self).__init__(self.ffi.chfl_frame(c_uint64(natoms)))

    def __del__(self):
        self.ffi.chfl_frame_free(self)

    def __copy__(self):
        return Frame.from_ptr(self.ffi.chfl_frame_copy(self))

    def atom(self, index):
        '''
        Get a specific :py:class:`Atom` from a frame, given its `index` in the
        frame
        '''
        ptr = self.ffi.chfl_atom_from_frame(self, c_uint64(index))
        if not ptr:
            raise IndexError("Not atom at index {} in frame".format(index))
        return Atom.from_ptr(ptr)

    def natoms(self):
        '''Get the current number of atoms in the :py:class:`Frame`.'''
        res = c_uint64()
        self.ffi.chfl_frame_atoms_count(self, res)
        return res.value

    def __len__(self):
        '''Get the current number of atoms in the :py:class:`Frame`.'''
        return self.natoms()

    def resize(self, size):
        '''Get the positions from the :py:class:`Frame`.'''
        self.ffi.chfl_frame_resize(self, c_uint64(size))

    def add_atom(self, atom, position, velocity=None):
        '''Get the positions from the :py:class:`Frame`.'''
        position = chfl_vector_t(position[0], position[1], position[2])
        if velocity:
            velocity = chfl_vector_t(velocity[0], velocity[1], velocity[2])
        self.ffi.chfl_frame_add_atom(self, atom, position, velocity)

    def remove(self, i):
        '''Remove the atom at index `i` in the :py:class:`Frame`.'''
        self.ffi.chfl_frame_remove(self, c_uint64(i))

    def positions(self):
        '''Get a view into the positions of the :py:class:`Frame`.'''
        natoms = c_uint64()
        data = POINTER(chfl_vector_t)()
        self.ffi.chfl_frame_positions(self, byref(data), byref(natoms))
        positions = np.ctypeslib.as_array(data, shape=(natoms.value,))
        return positions.view(np.float64).reshape((natoms.value, 3))

    def velocities(self):
        '''Get a view into the velocities of the :py:class:`Frame`.'''
        natoms = c_uint64()
        data = POINTER(chfl_vector_t)()
        self.ffi.chfl_frame_velocities(self, byref(data), byref(natoms))
        velocities = np.ctypeslib.as_array(data, shape=(natoms.value,))
        return velocities.view(np.float64).reshape((natoms.value, 3))

    def add_velocities(self):
        '''Add velocity information to this :py:class:`Frame`'''
        self.ffi.chfl_frame_add_velocities(self)

    def has_velocities(self):
        '''Check if the :py:class:`Frame` has velocity information.'''
        res = c_bool()
        self.ffi.chfl_frame_has_velocities(self, byref(res))
        return res.value

    def cell(self):
        '''Get the :py:class:`UnitCell` from the :py:class:`Frame`'''
        return UnitCell.from_ptr(self.ffi.chfl_cell_from_frame(self))

    def set_cell(self, cell):
        '''Set the :py:class:`UnitCell` of the :py:class:`Frame`'''
        self.ffi.chfl_frame_set_cell(self, cell)

    def topology(self):
        '''Get the :py:class:`Topology` from the :py:class:`Frame`'''
        return Topology.from_ptr(self.ffi.chfl_topology_from_frame(self))

    def set_topology(self, topology):
        '''Set the :py:class:`Topology` of the :py:class:`Frame`'''
        self.ffi.chfl_frame_set_topology(self, topology)

    def step(self):
        '''
        Get the :py:class:`Frame` step, i.e. the frame number in the trajectory
        '''
        res = c_uint64()
        self.ffi.chfl_frame_step(self, byref(res))
        return res.value

    def set_step(self, step):
        '''Set the :py:class:`Frame` step'''
        self.ffi.chfl_frame_set_step(self, c_uint64(step))

    def guess_topology(self, bonds=True):
        '''
        Try to guess the bonds, angles and dihedrals in the system. If
        ``bonds`` is True, guess everything; else only guess the angles and
        dihedrals from the topology bond list.
        '''
        self.ffi.chfl_frame_guess_topology(self, c_bool(bonds))
