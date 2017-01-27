# -*- coding=utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals
import numpy as np
from ctypes import c_double, c_int, byref
from enum import IntEnum

from chemfiles import get_c_library
from chemfiles.ffi import CHFL_CELL_TYPES
from chemfiles.errors import _check_handle


class CellType(IntEnum):
    '''
    Available cell types in Chemfiles:

    - ``CellType.Orthorhombic``: The three angles are 90°
    - ``CellType.Triclinic``: The three angles may not be 90°
    - ``CellType.Infinite``: Cell type when there is no periodic boundary
      conditions
    '''

    Orthorhombic = CHFL_CELL_TYPES.CHFL_CELL_ORTHORHOMBIC
    Triclinic = CHFL_CELL_TYPES.CHFL_CELL_TRICLINIC
    Infinite = CHFL_CELL_TYPES.CHFL_CELL_INFINITE


class UnitCell(object):
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
        self.c_lib = get_c_library()
        if alpha == 90.0 and beta == 90.0 and gamma == 90.0:
            a, b, c = c_double(a), c_double(b), c_double(c)
            self._handle_ = self.c_lib.chfl_cell(a, b, c)
        else:
            self._handle_ = self.c_lib.chfl_cell_triclinic(
                c_double(a), c_double(b), c_double(c),
                c_double(alpha), c_double(beta), c_double(gamma)
            )
        _check_handle(self._handle_)

    def __del__(self):
        c_lib = get_c_library()
        c_lib.chfl_cell_free(self._handle_)

    def lengths(self):
        '''Get the three lenghts of an :py:class:`UnitCell`, in Angstroms.'''
        a, b, c = c_double(), c_double(), c_double()
        self.c_lib.chfl_cell_lengths(
            self._handle_, byref(a), byref(b), byref(c)
        )
        return a.value, b.value, c.value

    def set_lengths(self, a, b, c):
        '''Set the three lenghts of an :py:class:`UnitCell`, in Angstroms.'''
        self.c_lib.chfl_cell_set_lengths(
            self._handle_, c_double(a), c_double(b), c_double(c)
        )

    def angles(self):
        '''Get the three angles of an :py:class:`UnitCell`, in degrees.'''
        alpha, beta, gamma = c_double(), c_double(), c_double()
        self.c_lib.chfl_cell_angles(
            self._handle_, byref(alpha), byref(beta), byref(gamma)
        )
        return alpha.value, beta.value, gamma.value

    def set_angles(self, alpha, beta, gamma):
        '''
        Set the three angles of an :py:class:`UnitCell`, in degrees. This is
        only possible for ``CellType.Triclinic`` cells.
        '''
        self.c_lib.chfl_cell_set_angles(
            self._handle_, c_double(alpha), c_double(beta), c_double(gamma)
        )

    def matrix(self):
        '''Get the unit cell matricial representation.'''
        res = np.zeros((3, 3), np.float64)
        self.c_lib.chfl_cell_matrix(self._handle_, res)
        return res

    def type(self):
        '''Get the type of the unit cell'''
        res = CHFL_CELL_TYPES()
        self.c_lib.chfl_cell_type(self._handle_, byref(res))
        return CellType(res.value)

    def set_type(self, celltype):
        '''Set the type of the unit cell'''
        self.c_lib.chfl_cell_set_type(self._handle_, c_int(celltype))

    def volume(self):
        '''Get the volume of the unit cell'''
        V = c_double()
        self.c_lib.chfl_cell_volume(self._handle_, byref(V))
        return V.value
