# -*- coding=utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals
import numpy as np
from ctypes import c_size_t, c_float, c_bool, POINTER, byref

from .ffi import c_lib
from .errors import _check_handle, ChemharpException, ArgumentError
from .cell import UnitCell
from .atom import Atom
from .topology import Topology


class Frame(object):
    '''
    A `Frame` holds data from one step of a simulation: the current `Topology`,
    the positions, and maybe the velocities of the particles in the system.
    '''

    def __init__(self, natoms=0):
        '''
        Create an empty frame with initial capacity of `natoms`. It will be
        resized by the library as needed.
        '''
        self._handle_ = c_lib.chrp_frame(c_size_t(natoms))
        _check_handle(self._handle_)

    def __del__(self):
        c_lib.chrp_frame_free(self._handle_)

    def atom(self, index):
        '''
        Get a specific ``Atom`` from a frame, given its `index` in the frame
        '''
        atom = Atom("")
        c_lib.chrp_atom_free(atom._handle_)
        atom._handle_ = c_lib.chrp_atom_from_frame(
            self._handle_, c_size_t(index)
        )
        try:
            _check_handle(atom._handle_)
        except ChemharpException:
            raise IndexError("Not atom at index {} in frame".format(index))
        return atom

    def natoms(self):
        '''Get the current number of atoms in the ``Frame``.'''
        res = c_size_t()
        c_lib.chrp_frame_atoms_count(self._handle_, res)
        return res.value

    def __len__(self):
        '''Get the current number of atoms in the ``Frame``.'''
        return self.natoms()

    def positions(self):
        '''Get the positions from the ``Frame``.'''
        natoms = self.natoms()
        res = np.zeros((natoms, 3), np.float32)
        c_lib.chrp_frame_positions(self._handle_, res, c_size_t(natoms))
        return res

    def set_positions(self, positions):
        '''Set the positions in the ``Frame``.'''
        shape = positions.shape
        if shape[1] != 3:
            raise ArgumentError("The positions array should have a Nx3 shape")
        if positions.dtype != np.float32:
            raise ArgumentError("The positions array should contain float32")
        c_lib.chrp_frame_set_positions(
            self._handle_,
            positions,
            c_size_t(shape[0])
        )

    def velocities(self):
        '''Get the velocities from the ``Frame``.'''
        natoms = self.natoms()
        res = np.zeros((natoms, 3), np.float32)
        c_lib.chrp_frame_velocities(self._handle_, res, c_size_t(natoms))
        return res

    def set_velocities(self, velocities):
        '''Set the velocities in the ``Frame``.'''
        shape = velocities.shape
        if shape[1] != 3:
            raise ArgumentError("The velocities array should have a Nx3 shape")
        if velocities.dtype != np.float32:
            raise ArgumentError("The velocities array should contain float32")
        c_lib.chrp_frame_set_velocities(
            self._handle_,
            velocities,
            c_size_t(shape[0])
        )

    def has_velocities(self):
        '''Check if the ``Frame`` has velocity information.'''
        res = c_bool()
        c_lib.chrp_frame_has_velocities(self._handle_, byref(res))
        return res.value

    def cell(self):
        '''Get the `UnitCell` from the ``Frame``'''
        cell = UnitCell(0, 0, 0)
        c_lib.chrp_cell_free(cell._handle_)
        cell._handle_ = c_lib.chrp_cell_from_frame(self._handle_)
        _check_handle(cell._handle_)
        return cell

    def set_cell(self, cell):
        '''Set the `UnitCell` of the `Frame`'''
        c_lib.chrp_frame_set_cell(self._handle_, cell._handle_)

    def topology(self):
        '''Get the ``Topology`` from the ``Frame``'''
        topology = Topology()
        c_lib.chrp_topology_free(topology._handle_)
        topology._handle_ = c_lib.chrp_topology_from_frame(self._handle_)
        _check_handle(topology._handle_)
        return topology

    def set_topology(self, topology):
        '''Set the `Topology` of the `Frame`'''
        c_lib.chrp_frame_set_topology(self._handle_, topology._handle_)

    def step(self):
        '''Get the ``Frame`` step, i.e. the frame number in the trajectory'''
        res = c_size_t()
        c_lib.chrp_frame_step(self._handle_, byref(res))
        return res.value

    def set_step(self, step):
        '''Set the ``Frame`` step'''
        c_lib.chrp_frame_set_step(self._handle_, c_size_t(step))

    def guess_topology(self, bonds=True):
        '''
        Try to guess the bonds, angles and dihedrals in the system. If
        ``bonds`` is True, guess everything; else only guess the angles and
        dihedrals from the topology bond list.
        '''
        c_lib.chrp_frame_guess_topology(self._handle_, c_bool(bonds))
