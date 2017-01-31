# -*- coding=utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals
from ctypes import c_double, ARRAY
from enum import IntEnum

from chemfiles.types import CxxPointer
from chemfiles.ffi import chfl_cell_shape_t, chfl_vector_t


class CellShape(IntEnum):
    '''
    Available cell types in Chemfiles:

    - ``CellType.Orthorhombic``: The three angles are 90°
    - ``CellType.Triclinic``: The three angles may not be 90°
    - ``CellType.Infinite``: Cell type when there is no periodic boundary
      conditions
    '''

    Orthorhombic = chfl_cell_shape_t.CHFL_CELL_ORTHORHOMBIC
    Triclinic = chfl_cell_shape_t.CHFL_CELL_TRICLINIC
    Infinite = chfl_cell_shape_t.CHFL_CELL_INFINITE


class UnitCell(CxxPointer):
    '''
    An :py:class:`UnitCell` represent the box containing the atoms in the
    system, and its periodicity.

    A unit cell is fully represented by three lenghts (a, b, c); and three
    angles (alpha, beta, gamma). The angles are stored in degrees, and the
    lenghts in Angstroms. A cell also has a matricial representation, by
    projecting the three base vector into an orthonormal base. We choose to
    represent such matrix as an upper triangular matrix::

                | a_x   b_x   c_x |
                |  0    b_y   c_y |
                |  0     0    c_z |

    An unit cell also have a cell type, represented by the :py:class:`CellType`
    class.
    '''

    def __init__(self, a, b, c, alpha=90.0, beta=90.0, gamma=90.0):
        '''
        Create a new :py:class:`UnitCell` with cell lenghts of ``a``, ``b`` and
        ``c``, and cell angles ``alpha``, ``beta`` and ``gamma``.
        '''
        lenghts = chfl_vector_t(a, b, c)
        angles = chfl_vector_t(alpha, beta, gamma)
        if alpha == 90.0 and beta == 90.0 and gamma == 90.0:
            ptr = self.ffi.chfl_cell(lenghts)
        else:
            ptr = self.ffi.chfl_cell_triclinic(lenghts, angles)
        super(UnitCell, self).__init__(ptr)

    def __del__(self):
        self.ffi.chfl_cell_free(self)

    def __copy__(self):
        return UnitCell.from_ptr(self.ffi.chfl_cell_copy(self))

    def lengths(self):
        '''Get the three lenghts of an :py:class:`UnitCell`, in Angstroms.'''
        lengths = chfl_vector_t(0, 0, 0)
        self.ffi.chfl_cell_lengths(self, lengths)
        return lengths[0], lengths[1], lengths[2]

    def set_lengths(self, a, b, c):
        '''Set the three lenghts of an :py:class:`UnitCell`, in Angstroms.'''
        self.ffi.chfl_cell_set_lengths(self, chfl_vector_t(a, b, c))

    def angles(self):
        '''Get the three angles of an :py:class:`UnitCell`, in degrees.'''
        angles = chfl_vector_t(0, 0, 0)
        self.ffi.chfl_cell_angles(self, angles)
        return angles[0], angles[1], angles[2]

    def set_angles(self, alpha, beta, gamma):
        '''
        Set the three angles of an :py:class:`UnitCell`, in degrees. This is
        only possible for ``CellType.Triclinic`` cells.
        '''
        self.ffi.chfl_cell_set_angles(
            self, chfl_vector_t(alpha, beta, gamma)
        )

    def matrix(self):
        '''Get the unit cell matricial representation.'''
        m = ARRAY(chfl_vector_t, 3)()
        self.ffi.chfl_cell_matrix(self, m)
        return [
            (m[0][0], m[0][1], m[0][2]),
            (m[1][0], m[1][1], m[1][2]),
            (m[2][0], m[2][1], m[2][2]),
        ]

    def shape(self):
        '''Get the type of the unit cell'''
        shape = chfl_cell_shape_t()
        self.ffi.chfl_cell_shape(self, shape)
        return CellShape(shape.value)

    def set_shape(self, shape):
        '''Set the type of the unit cell'''
        self.ffi.chfl_cell_set_shape(self, chfl_cell_shape_t(shape))

    def volume(self):
        '''Get the volume of the unit cell'''
        volume = c_double()
        self.ffi.chfl_cell_volume(self, volume)
        return volume.value
