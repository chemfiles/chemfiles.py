# -*- coding=utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals
import numpy as np
from ctypes import c_uint64, c_bool, c_double, POINTER

from ._utils import CxxPointer, string_type
from .misc import ChemfilesError
from .ffi import chfl_vector3d
from .atom import Atom
from .topology import Topology
from .cell import UnitCell
from .property import Property


class FrameAtoms(object):
    """Proxy object to get the atoms in a frame"""

    def __init__(self, frame):
        self.frame = frame

    def __len__(self):
        """Get the current number of atoms in this :py:class:`Frame`."""
        count = c_uint64()
        self.frame.ffi.chfl_frame_atoms_count(self.frame, count)
        return count.value

    def __getitem__(self, index):
        """
        Get a reference to the :py:class:`Atom` at the given ``index`` in the
        associated :py:class:`Frame`.
        """
        if index >= len(self):
            raise IndexError("atom index ({}) out of range for this frame".format(index))
        else:
            ptr = self.frame.ffi.chfl_atom_from_frame(self.frame, c_uint64(index))
            return Atom.from_ptr(ptr)

    def __iter__(self):
        for i in range(len(self)):
            yield self[i]


class Frame(CxxPointer):
    """
    A :py:class:`Frame` contains data from one simulation step: the current
    unit cell, the topology, the positions, and the velocities of the particles
    in the system. If some information is missing (topology or velocity or unit
    cell), the corresponding data is filled with a default value.
    """

    def __init__(self):
        """
        Create an empty :py:class:`Frame` that will be resized by the runtime
        as needed.
        """
        super(Frame, self).__init__(self.ffi.chfl_frame(), is_const=False)

    def __copy__(self):
        return Frame.from_ptr(self.ffi.chfl_frame_copy(self))

    @property
    def atoms(self):
        return FrameAtoms(self)

    def resize(self, count):
        """
        Resize the positions, velocities and topology in this
        :py:class:`Frame`, to have space for `count` atoms.

        This function may invalidate any array of the positions or the
        velocities if the new size is bigger than the old one. In all cases,
        previous data is conserved. This function conserve the presence or
        absence of velocities.
        """
        self.ffi.chfl_frame_resize(self, c_uint64(count))

    def add_atom(self, atom, position, velocity=None):
        """
        Add a copy of the :py:class:`Atom` ``atom`` and the corresponding
        ``position`` and ``velocity`` to this :py:class:`Frame`.

        ``velocity`` can be ``None`` if no velocity is associated with the
        atom.
        """
        position = chfl_vector3d(position[0], position[1], position[2])
        if velocity:
            velocity = chfl_vector3d(velocity[0], velocity[1], velocity[2])
        self.ffi.chfl_frame_add_atom(self, atom, position, velocity)

    def remove(self, i):
        """
        Remove the atom at index ``i`` in this :py:class:`Frame`.

        This modify all the atoms indexes after ``i``, and invalidate any array
        obtained using :py:func:`Frame.positions` or
        :py:func:`Frame.velocities`.
        """
        self.ffi.chfl_frame_remove(self, c_uint64(i))

    def add_bond(self, i, j):
        """
        Add a bond between the atoms at indexes ``i`` and ``j`` in this
        :py:class:`Frame`'s topology.
        """
        self.ffi.chfl_frame_add_bond(self, c_uint64(i), c_uint64(j))

    def remove_bond(self, i, j):
        """
        Remove any existing bond between the atoms at indexes ``i`` and ``j``
        in this :py:class:`Frame`'s topology.

        This function does nothing if there is no bond between ``i`` and ``j``.
        """
        self.ffi.chfl_frame_remove_bond(self, c_uint64(i), c_uint64(j))

    def add_residue(self, residue):
        """
        Add the :py:class:`Residue` ``residue`` to this :py:class:`Frame`'s
        topology.

        The residue ``id`` must not already be in the topology, and the residue
        must contain only atoms that are not already in another residue.
        """
        self.ffi.chfl_frame_add_residue(self, residue)

    @property
    def positions(self):
        """
        Get a view into the positions of this :py:class:`Frame`.

        This function gives direct access to the positions as a numpy array.
        Modifying the array will change the positions in the frame.

        If the frame is resized (by writing to it, calling
        :py:func:`Frame.resize`, :py:func:`Frame.add_atom`,
        :py:func:`Frame.remove`), the array is invalidated. Accessing it can
        cause a segfault.
        """
        count = c_uint64()
        data = POINTER(chfl_vector3d)()
        self.ffi.chfl_frame_positions(self, data, count)
        count = count.value
        if count != 0:
            positions = np.ctypeslib.as_array(data, shape=(count,))
            return positions.view(np.float64).reshape((count, 3))
        else:
            return np.array([[], [], []], dtype=np.float64)

    @property
    def velocities(self):
        """
        Get a view into the velocities of this :py:class:`Frame`.

        This function gives direct access to the velocities as a numpy array.
        Modifying the array will change the velocities in the frame.

        If the frame is resized (by writing to it, calling
        :py:func:`Frame.resize`, :py:func:`Frame.add_atom`,
        :py:func:`Frame.remove`), the array is invalidated. Accessing it can
        cause a segfault.
        """
        count = c_uint64()
        data = POINTER(chfl_vector3d)()
        self.ffi.chfl_frame_velocities(self, data, count)
        count = count.value
        if count != 0:
            positions = np.ctypeslib.as_array(data, shape=(count,))
            return positions.view(np.float64).reshape((count, 3))
        else:
            return np.array([[], [], []], dtype=np.float64)

    def add_velocities(self):
        """
        Add velocity data to this :py:class:`Frame`.

        The velocities are initialized to zero. If the frame already contains
        velocities, this function does nothing.
        """
        self.ffi.chfl_frame_add_velocities(self)

    def has_velocities(self):
        """Check if this :py:class:`Frame` contains velocity."""
        velocities = c_bool()
        self.ffi.chfl_frame_has_velocities(self, velocities)
        return velocities.value

    @property
    def cell(self):
        """
        Get a mutable reference to the :py:class:`UnitCell` of this
        :py:class:`Frame`. Any modification to the cell will be reflected in
        the frame.
        """
        return UnitCell.from_ptr(self.ffi.chfl_cell_from_frame(self))

    @cell.setter
    def cell(self, cell):
        """
        Set the :py:class:`UnitCell` of this :py:class:`Frame` to ``cell``.
        """
        self.ffi.chfl_frame_set_cell(self, cell)

    @property
    def topology(self):
        """
        Get read-only access to the :py:class:`Topology` of this
        :py:class:`Frame`.
        """
        return Topology.from_const_ptr(self.ffi.chfl_topology_from_frame(self))

    @topology.setter
    def topology(self, topology):
        """
        Set the :py:class:`Topology` of this :py:class:`Frame` to ``topology``.
        """
        self.ffi.chfl_frame_set_topology(self, topology)

    @property
    def step(self):
        """
        Get this :py:class:`Frame` step, i.e. the frame number in the
        trajectory.
        """
        step = c_uint64()
        self.ffi.chfl_frame_step(self, step)
        return step.value

    @step.setter
    def step(self, step):
        """Set this :py:class:`Frame` step to ``step``."""
        self.ffi.chfl_frame_set_step(self, c_uint64(step))

    def guess_bonds(self):
        """
        Guess the bonds, angles and dihedrals in this :py:class:`Frame`.

        The bonds are guessed using a distance-based algorithm, and then angles
        and dihedrals are guessed from the bonds.
        """
        self.ffi.chfl_frame_guess_bonds(self)

    def distance(self, i, j):
        """
        Get the distance between the atoms at indexes ``i`` and ``j`` in this
        :py:class:`Frame`, accounting for periodic boundary conditions. The
        result is expressed in angstroms.
        """
        distance = c_double()
        self.ffi.chfl_frame_distance(self, c_uint64(i), c_uint64(j), distance)
        return distance.value

    def angle(self, i, j, k):
        """
        Get the angle formed by the atoms at indexes ``i``, ``j`` and ``k`` in
        this :py:class:`Frame`, accounting for periodic boundary conditions.
        The result is expressed in radians.
        """
        angle = c_double()
        self.ffi.chfl_frame_angle(self, c_uint64(i), c_uint64(j), c_uint64(k), angle)
        return angle.value

    def dihedral(self, i, j, k, m):
        """
        Get the dihedral angle formed by the atoms at indexes ``i``, ``j``,
        ``k`` and ``m`` in this :py:class:`Frame`, accounting for periodic
        boundary conditions. The result is expressed in radians.
        """
        dihedral = c_double()
        self.ffi.chfl_frame_dihedral(
            self, c_uint64(i), c_uint64(j), c_uint64(k), c_uint64(m), dihedral
        )
        return dihedral.value

    def out_of_plane(self, i, j, k, m):
        """
        Get the out of plane distance formed by the atoms at indexes ``i``,
        ``j``, ``k`` and ``m`` in this :py:class:`Frame`, accounting for
        periodic boundary conditions. The result is expressed in angstroms.

        This is the distance betweent the atom j and the ikm plane. The j atom
        is the center of the improper dihedral angle formed by i, j, k and m.
        """
        distance = c_double()
        self.ffi.chfl_frame_out_of_plane(
            self, c_uint64(i), c_uint64(j), c_uint64(k), c_uint64(m), distance
        )
        return distance.value

    def __iter__(self):
        # Disable automatic iteration from __getitem__
        raise TypeError("use Frame.atoms to iterate over a frame")

    def __getitem__(self, name):
        """
        Get a property of this frame with the given ``name``, or raise an error
        if the property does not exists.
        """
        if not isinstance(name, string_type):
            raise ChemfilesError(
                "Invalid type {} for a frame property name".format(type(name))
            )
        ptr = self.ffi.chfl_frame_get_property(self, name.encode("utf8"))
        return Property.from_ptr(ptr).get()

    def __setitem__(self, name, value):
        """
        Set a property of this frame, with the given ``name`` and ``value``.
        The new value overwrite any pre-existing property with the same name.
        """
        if not isinstance(name, string_type):
            raise ChemfilesError(
                "Invalid type {} for a frame property name".format(type(name))
            )
        self.ffi.chfl_frame_set_property(self, name.encode("utf8"), Property(value))