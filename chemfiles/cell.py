# -*- coding=utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals
from ctypes import c_double, ARRAY
from enum import IntEnum

from .utils import CxxPointer
from .ffi import chfl_cellshape, chfl_vector3d


class CellShape(IntEnum):
    '''
    Available cell shapes in Chemfiles:

    - ``CellType.Orthorhombic``: for cells where the three angles are 90°;
    - ``CellType.Triclinic``: for cells where the three angles may not be 90°;
    - ``CellType.Infinite``: for cells without periodic boundary conditions;
    '''

    Orthorhombic = chfl_cellshape.CHFL_CELL_ORTHORHOMBIC
    Triclinic = chfl_cellshape.CHFL_CELL_TRICLINIC
    Infinite = chfl_cellshape.CHFL_CELL_INFINITE


class UnitCell(CxxPointer):
    '''
    An :py:class:`UnitCell` represent the box containing the atoms, and its
    periodicity.

    An unit cell is fully represented by three lenghts (a, b, c); and three
    angles (alpha, beta, gamma). The angles are stored in degrees, and the
    lenghts in Angstroms. The cell angles are defined as follow: alpha is the
    angles between the cell vectors `b` and `c`; beta as the angle between `a`
    and `c`; and gamma as the angle between `a` and `b`.

    A cell also has a matricial representation, by projecting the three base
    vector into an orthonormal base. We choose to represent such matrix as an
    upper triangular matrix:

    .. code-block:: sh

        | a_x   b_x   c_x |
        |  0    b_y   c_y |
        |  0     0    c_z |
    '''

    def __init__(self, a, b, c, alpha=90.0, beta=90.0, gamma=90.0):
        '''
        Create a new :py:class:`UnitCell` with cell lenghts of ``a``, ``b`` and
        ``c``, and cell angles ``alpha``, ``beta`` and ``gamma``.

        If alpha, beta and gamma are equal to 90.0, the new unit cell shape is
        ``CellShape.Orthorhombic``. Else it is ``CellShape.Infinite``.
        '''
        lenghts = chfl_vector3d(a, b, c)
        angles = chfl_vector3d(alpha, beta, gamma)
        if alpha == 90.0 and beta == 90.0 and gamma == 90.0:
            ptr = self.ffi.chfl_cell(lenghts)
        else:
            ptr = self.ffi.chfl_cell_triclinic(lenghts, angles)
        super(UnitCell, self).__init__(ptr)

    def __del__(self):
        if hasattr(self, 'ptr'):
            self.ffi.chfl_cell_free(self)

    def __copy__(self):
        return UnitCell.from_ptr(self.ffi.chfl_cell_copy(self))

    def lengths(self):
        '''Get the three lenghts of this :py:class:`UnitCell`, in Angstroms.'''
        lengths = chfl_vector3d(0, 0, 0)
        self.ffi.chfl_cell_lengths(self, lengths)
        return lengths[0], lengths[1], lengths[2]

    def set_lengths(self, a, b, c):
        '''
        Set the three lenghts of this :py:class:`UnitCell` to ``a``, ``b`` and
        ``c``. These values should be in Angstroms.
        '''
        self.ffi.chfl_cell_set_lengths(self, chfl_vector3d(a, b, c))

    def angles(self):
        '''Get the three angles of this :py:class:`UnitCell`, in degrees.'''
        angles = chfl_vector3d(0, 0, 0)
        self.ffi.chfl_cell_angles(self, angles)
        return angles[0], angles[1], angles[2]

    def set_angles(self, alpha, beta, gamma):
        '''
        Set the three angles of this :py:class:`UnitCell` to ``alpha``,
        ``beta`` and ``gamma``. These values should be in degrees. Setting
        angles is only possible for ``CellShape.Triclinic`` cells.
        '''
        self.ffi.chfl_cell_set_angles(
            self, chfl_vector3d(alpha, beta, gamma)
        )

    def matrix(self):
        '''
        Get this :py:class:`UnitCell` matricial representation.

        The matricial representation is obtained by aligning the a vector along
        the *x* axis and putting the b vector in the *xy* plane. This make the
        matrix an upper triangular matrix:

        .. code-block:: sh

            | a_x   b_x   c_x |
            |  0    b_y   c_y |
            |  0     0    c_z |
        '''
        m = ARRAY(chfl_vector3d, 3)()
        self.ffi.chfl_cell_matrix(self, m)
        return [
            (m[0][0], m[0][1], m[0][2]),
            (m[1][0], m[1][1], m[1][2]),
            (m[2][0], m[2][1], m[2][2]),
        ]

    def shape(self):
        '''Get the shape of this :py:class:`UnitCell`.'''
        shape = chfl_cellshape()
        self.ffi.chfl_cell_shape(self, shape)
        return CellShape(shape.value)

    def set_shape(self, shape):
        '''Set the shape of this :py:class:`UnitCell` to ``shape``.'''
        self.ffi.chfl_cell_set_shape(self, chfl_cellshape(shape))

    def volume(self):
        '''Get the volume of this :py:class:`UnitCell`.'''
        volume = c_double()
        self.ffi.chfl_cell_volume(self, volume)
        return volume.value

    def wrap(self, vector):
        '''
        Wrap a ``vector`` in this :py:class:`UnitCell`, and return the wrapped
        vector.
        '''
        vector = chfl_vector3d(vector[0], vector[1], vector[2])
        self.ffi.chfl_cell_wrap(self, vector)
        return (vector[0], vector[1], vector[2])
