# -*- coding=utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals
import numpy as np
from ctypes import c_uint64, c_bool, c_double, POINTER

from .ffi import chfl_vector3d
from .utils import CxxPointer
from .atom import Atom
from .topology import Topology
from .cell import UnitCell
from .property import Property


class Frame(CxxPointer):
    '''
    A :py:class:`Frame` contains data from one simulation step: the current
    unit cell, the topology, the positions, and the velocities of the particles
    in the system. If some information is missing (topology or velocity or unit
    cell), the corresponding data is filled with a default value.
    '''

    def __init__(self):
        '''
        Create an empty :py:class:`Frame` that will be resized by the runtime
        as needed.
        '''
        super(Frame, self).__init__(self.ffi.chfl_frame())

    def __del__(self):
        if hasattr(self, 'ptr'):
            self.ffi.chfl_frame_free(self)

    def __copy__(self):
        return Frame.from_ptr(self.ffi.chfl_frame_copy(self))

    def __iter__(self):
        for i in range(self.natoms()):
            yield self.atom(i)

    def atom(self, i):
        '''
        Get a copy of the :py:class:`Atom` at index ``i`` in this
        :py:class:`Frame`.
        '''
        if i >= self.natoms():
            raise IndexError(
                "atom index ({}) out of range for this frame".format(i)
            )
        return Atom.from_ptr(self.ffi.chfl_atom_from_frame(self, c_uint64(i)))

    def natoms(self):
        '''Get the current number of atoms in this :py:class:`Frame`.'''
        natoms = c_uint64()
        self.ffi.chfl_frame_atoms_count(self, natoms)
        return natoms.value

    def __len__(self):
        '''Get the current number of atoms in this :py:class:`Frame`.'''
        return self.natoms()

    def resize(self, natoms):
        '''
        Resize the positions, velocities  and topology in this
        :py:class:`Frame`, to have space for `natoms` atoms.

        This function may invalidate any array of the positions or the
        velocities if the new size is bigger than the old one. In all cases,
        previous data is conserved. This function conserve the presence or
        absence of velocities.
        '''
        self.ffi.chfl_frame_resize(self, c_uint64(natoms))

    def add_atom(self, atom, position, velocity=None):
        '''
        Add a copy of the :py:class:`Atom` ``atom`` and the corresponding
        ``position`` and ``velocity`` to this :py:class:`Frame`.

        ``velocity`` can be ``None`` if no velocity is associated with the
        atom.
        '''
        position = chfl_vector3d(position[0], position[1], position[2])
        if velocity:
            velocity = chfl_vector3d(velocity[0], velocity[1], velocity[2])
        self.ffi.chfl_frame_add_atom(self, atom, position, velocity)

    def remove(self, i):
        '''
        Remove the atom at index ``i`` in this :py:class:`Frame`.

        This modify all the atoms indexes after ``i``, and invalidate any array
        obtained using :py:func:`Frame.positions` or
        :py:func:`Frame.velocities`.
        '''
        self.ffi.chfl_frame_remove(self, c_uint64(i))

    def add_bond(self, i, j):
        '''
        Add a bond between the atoms at indexes ``i`` and ``j`` in this
        :py:class:`Frame`'s topology.
        '''
        self.ffi.chfl_frame_add_bond(self, c_uint64(i), c_uint64(j))

    def remove_bond(self, i, j):
        '''
        Remove any existing bond between the atoms at indexes ``i`` and ``j``
        in this :py:class:`Frame`'s topology.

        This function does nothing if there is no bond between ``i`` and ``j``.
        '''
        self.ffi.chfl_frame_remove_bond(self, c_uint64(i), c_uint64(j))

    def add_residue(self, residue):
        '''
        Add the :py:class:`Residue` ``residue`` to this :py:class:`Frame`'s
        topology.

        The residue ``id`` must not already be in the topology, and the residue
        must contain only atoms that are not already in another residue.
        '''
        self.ffi.chfl_frame_add_residue(self, residue)

    def positions(self):
        '''
        Get a view into the positions of this :py:class:`Frame`.

        Positions are stored as a `natoms x 3` array by thez runtime, this
        function gives direct access to the corresponding memory as a numpy
        array. Modifying the array will change the positions.

        If the frame is resized (by writing to it, calling
        :py:func:`Frame.resize`, :py:func:`Frame.add_atom`,
        :py:func:`Frame.remove`), the array is invalidated. Accessing it can
        cause a segfault.
        '''
        natoms = c_uint64()
        data = POINTER(chfl_vector3d)()
        self.ffi.chfl_frame_positions(self, data, natoms)
        natoms = natoms.value
        if natoms != 0:
            positions = np.ctypeslib.as_array(data, shape=(natoms,))
            return positions.view(np.float64).reshape((natoms, 3))
        else:
            return np.array([[], [], []], dtype=np.float64)

    def velocities(self):
        '''
        Get a view into the velocities of this :py:class:`Frame`.

        Velocities are stored as a `natoms x 3` array by thez runtime, this
        function gives direct access to the corresponding memory as a numpy
        array. Modifying the array will change the velocities.

        If the frame is resized (by writing to it, calling
        :py:func:`Frame.resize`, :py:func:`Frame.add_atom`,
        :py:func:`Frame.remove`), the array is invalidated. Accessing it can
        cause a segfault.
        '''
        natoms = c_uint64()
        data = POINTER(chfl_vector3d)()
        self.ffi.chfl_frame_velocities(self, data, natoms)
        natoms = natoms.value
        if natoms != 0:
            positions = np.ctypeslib.as_array(data, shape=(natoms,))
            return positions.view(np.float64).reshape((natoms, 3))
        else:
            return np.array([[], [], []], dtype=np.float64)

    def add_velocities(self):
        '''
        Add velocity data to this :py:class:`Frame`.

        The velocities are initialized to zero. If the frame already contains
        velocities, this function does nothing.
        '''
        self.ffi.chfl_frame_add_velocities(self)

    def has_velocities(self):
        '''Check if this :py:class:`Frame` contains velocity.'''
        velocities = c_bool()
        self.ffi.chfl_frame_has_velocities(self, velocities)
        return velocities.value

    def cell(self):
        '''Get a copy of the :py:class:`UnitCell` of this :py:class:`Frame`.'''
        return UnitCell.from_ptr(self.ffi.chfl_cell_from_frame(self))

    def set_cell(self, cell):
        '''
        Set the :py:class:`UnitCell` of this :py:class:`Frame` to ``cell``.
        '''
        self.ffi.chfl_frame_set_cell(self, cell)

    def topology(self):
        '''
        Get a copy of the :py:class:`Topology` of this :py:class:`Frame`.
        '''
        return Topology.from_ptr(self.ffi.chfl_topology_from_frame(self))

    def set_topology(self, topology):
        '''
        Set the :py:class:`Topology` of this :py:class:`Frame` to ``topology``.
        '''
        self.ffi.chfl_frame_set_topology(self, topology)

    def step(self):
        '''
        Get this :py:class:`Frame` step, i.e. the frame number in the
        trajectory.
        '''
        step = c_uint64()
        self.ffi.chfl_frame_step(self, step)
        return step.value

    def set_step(self, step):
        '''Set this :py:class:`Frame` step to ``step``.'''
        self.ffi.chfl_frame_set_step(self, c_uint64(step))

    def guess_topology(self):
        '''
        Guess the bonds, angles and dihedrals in this :py:class:`Frame`.

        The bonds are guessed using a distance-based algorithm, and then angles
        and dihedrals are guessed from the bonds.
        '''
        self.ffi.chfl_frame_guess_topology(self)

    def distance(self, i, j):
        '''
        Get the distance between the atoms at indexes ``i`` and ``j`` in this
        :py:class:`Frame`, accounting for periodic boundary conditions. The
        result is expressed in angstroms.
        '''
        distance = c_double()
        self.ffi.chfl_frame_distance(self, c_uint64(i), c_uint64(j), distance)
        return distance.value

    def angle(self, i, j, k):
        '''
        Get the angle formed by the atoms at indexes ``i``, ``j`` and ``k`` in
        this :py:class:`Frame`, accounting for periodic boundary conditions.
        The result is expressed in radians.
        '''
        angle = c_double()
        self.ffi.chfl_frame_angle(
            self, c_uint64(i), c_uint64(j), c_uint64(k), angle
        )
        return angle.value

    def dihedral(self, i, j, k, m):
        '''
        Get the dihedral angle formed by the atoms at indexes ``i``, ``j``,
        ``k`` and ``m`` in this :py:class:`Frame`, accounting for periodic
        boundary conditions. The result is expressed in radians.
        '''
        dihedral = c_double()
        self.ffi.chfl_frame_dihedral(
            self, c_uint64(i), c_uint64(j), c_uint64(k), c_uint64(m), dihedral
        )
        return dihedral.value

    def out_of_plane(self, i, j, k, m):
        '''
        Get the out of plane distance formed by the atoms at indexes ``i``,
        ``j``, ``k`` and ``m`` in this :py:class:`Frame`, accounting for
        periodic boundary conditions. The result is expressed in angstroms.

        This is the distance betweent the atom j and the ikm plane. The j atom
        is the center of the improper dihedral angle formed by i, j, k and m.
        '''
        distance = c_double()
        self.ffi.chfl_frame_out_of_plane(
            self, c_uint64(i), c_uint64(j), c_uint64(k), c_uint64(m), distance
        )
        return distance.value

    def set(self, name, value):
        '''
        Set a property of this frame, with the given ``name`` and ``value``.
        The new value overwrite any pre-existing property with the same name.
        '''
        self.ffi.chfl_frame_set_property(
            self, name.encode("utf8"), Property(value)
        )

    def get(self, name):
        '''
        Get a property of this frame with the given ``name``, or raise an error
        if the property does not exists.
        '''
        ptr = self.ffi.chfl_frame_get_property(self, name.encode("utf8"))
        return Property.from_ptr(ptr).get()
