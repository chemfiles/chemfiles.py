# -*- coding=utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals
import numpy as np
from ctypes import c_size_t, c_bool, c_float, byref, POINTER

from chemfiles import get_c_library
from chemfiles.errors import _check_handle, ChemfilesException
from chemfiles.cell import UnitCell
from chemfiles.atom import Atom
from chemfiles.topology import Topology


class Frame(object):
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
        self.c_lib = get_c_library()
        self._handle_ = self.c_lib.chfl_frame(c_size_t(natoms))
        _check_handle(self._handle_)

    def __del__(self):
        self.c_lib.chfl_frame_free(self._handle_)

    def atom(self, index):
        '''
        Get a specific :py:class:`Atom` from a frame, given its `index` in the
        frame
        '''
        atom = Atom("")
        self.c_lib.chfl_atom_free(atom._handle_)
        atom._handle_ = self.c_lib.chfl_atom_from_frame(
            self._handle_, c_size_t(index)
        )
        try:
            _check_handle(atom._handle_)
        except ChemfilesException:
            raise IndexError("Not atom at index {} in frame".format(index))
        return atom

    def natoms(self):
        '''Get the current number of atoms in the :py:class:`Frame`.'''
        res = c_size_t()
        self.c_lib.chfl_frame_atoms_count(self._handle_, res)
        return res.value

    def __len__(self):
        '''Get the current number of atoms in the :py:class:`Frame`.'''
        return self.natoms()

    def resize(self, size):
        '''Get the positions from the :py:class:`Frame`.'''
        self.c_lib.chfl_frame_resize(self._handle_, c_size_t(size))

    def positions(self):
        '''Get a view into the positions of the :py:class:`Frame`.'''
        natoms = c_size_t()
        data = POINTER(c_float)()
        self.c_lib.chfl_frame_positions(
            self._handle_, byref(data), byref(natoms)
        )
        return np.ctypeslib.as_array(data, shape=(natoms.value, 3))

    def velocities(self):
        '''Get a view into the velocities of the :py:class:`Frame`.'''
        natoms = c_size_t()
        data = POINTER(c_float)()
        self.c_lib.chfl_frame_velocities(
            self._handle_, byref(data), byref(natoms)
        )
        return np.ctypeslib.as_array(data, shape=(natoms.value, 3))

    def add_velocities(self):
        '''Add velocity information to this :py:class:`Frame`'''
        self.c_lib.chfl_frame_add_velocities(self._handle_)

    def has_velocities(self):
        '''Check if the :py:class:`Frame` has velocity information.'''
        res = c_bool()
        self.c_lib.chfl_frame_has_velocities(self._handle_, byref(res))
        return res.value

    def cell(self):
        '''Get the :py:class:`UnitCell` from the :py:class:`Frame`'''
        cell = UnitCell(0, 0, 0)
        self.c_lib.chfl_cell_free(cell._handle_)
        cell._handle_ = self.c_lib.chfl_cell_from_frame(self._handle_)
        _check_handle(cell._handle_)
        return cell

    def set_cell(self, cell):
        '''Set the :py:class:`UnitCell` of the :py:class:`Frame`'''
        self.c_lib.chfl_frame_set_cell(self._handle_, cell._handle_)

    def topology(self):
        '''Get the :py:class:`Topology` from the :py:class:`Frame`'''
        topology = Topology()
        self.c_lib.chfl_topology_free(topology._handle_)
        topology._handle_ = self.c_lib.chfl_topology_from_frame(self._handle_)
        _check_handle(topology._handle_)
        return topology

    def set_topology(self, topology):
        '''Set the :py:class:`Topology` of the :py:class:`Frame`'''
        self.c_lib.chfl_frame_set_topology(self._handle_, topology._handle_)

    def step(self):
        '''
        Get the :py:class:`Frame` step, i.e. the frame number in the trajectory
        '''
        res = c_size_t()
        self.c_lib.chfl_frame_step(self._handle_, byref(res))
        return res.value

    def set_step(self, step):
        '''Set the :py:class:`Frame` step'''
        self.c_lib.chfl_frame_set_step(self._handle_, c_size_t(step))

    def guess_topology(self, bonds=True):
        '''
        Try to guess the bonds, angles and dihedrals in the system. If
        ``bonds`` is True, guess everything; else only guess the angles and
        dihedrals from the topology bond list.
        '''
        self.c_lib.chfl_frame_guess_topology(self._handle_, c_bool(bonds))
