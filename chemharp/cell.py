# -*- coding=utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals
import numpy as np
from ctypes import c_double, c_bool, c_int, byref, POINTER
from enum import IntEnum

from .ffi import get_c_library, CHRP_CELL_TYPES
from .errors import _check_handle


class CellType(IntEnum):
    '''
    Possibles values for the cell type:
        - NONE: Do not log anything
        - ERROR: Only log errors
        - WARNING: Log errors and warnings
        - INFO: Log errors, warnings and informations
        - DEBUG: Log everything, from errors to debug informations
    '''

    Orthorombic = CHRP_CELL_TYPES.CHRP_CELL_ORTHOROMBIC
    Triclinic = CHRP_CELL_TYPES.CHRP_CELL_TRICLINIC
    Infinite = CHRP_CELL_TYPES.CHRP_CELL_INFINITE

    @classmethod
    def _from_int(cls, value):
        if value == CHRP_CELL_TYPES.CHRP_CELL_ORTHOROMBIC:
            return CellType.Orthorombic
        elif value == CHRP_CELL_TYPES.CHRP_CELL_TRICLINIC:
            return CellType.Triclinic
        elif value == CHRP_CELL_TYPES.CHRP_CELL_INFINITE:
            return CellType.Infinite
        else:
            raise ValueError(
                "Invalid CHRP_CELL_TYPES enum variant: {}".format(value)
            )


class UnitCell(object):
    '''
    An ``UnitCell`` represent the box containing the atoms in the system, and
    its periodicity.

    A unit cell is fully represented by three lenghts (a, b, c); and three
    angles (alpha, beta, gamma). The angles are stored in degrees, and the
    lenghts in Angstroms. A cell also has a matricial representation, by
    projecting the three base vector into an orthonormal base. We choose to
    represent such matrix as an upper triangular matrix:

                | a_x   b_x   c_x |
                |  0    b_y   c_y |
                |  0     0    c_z |

    An unit cell also have a cell type, represented by the `CellType` class.
    '''

    def __init__(self, a, b, c, alpha=90.0, beta=90.0, gamma=90.0):
        '''
        Create a new ``UnitCell`` with cell lenghts of ``a``, ``b`` and ``c``,
        and cell angles ``alpha``, ``beta`` and ``gamma``.
        '''
        self.c_lib = get_c_library()
        if alpha == 90.0 and beta == 90.0 and gamma == 90.0:
            a, b, c = c_double(a), c_double(b), c_double(c)
            self._handle_ = self.c_lib.chrp_cell(a, b, c)
        else:
            self._handle_ = self.c_lib.chrp_cell_triclinic(
                c_double(a), c_double(b), c_double(c),
                c_double(alpha), c_double(beta), c_double(gamma)
            )
        _check_handle(self._handle_)

    def __del__(self):
        self.c_lib.chrp_cell_free(self._handle_)

    def lengths(self):
        '''Get the three lenghts of an ``UnitCell``, in Angstroms.'''
        a, b, c = c_double(), c_double(), c_double()
        self.c_lib.chrp_cell_lengths(
            self._handle_, byref(a), byref(b), byref(c)
        )
        return a.value, b.value, c.value

    def set_lengths(self, a, b, c):
        '''Set the three lenghts of an ``UnitCell``, in Angstroms.'''
        self.c_lib.chrp_cell_set_lengths(
            self._handle_, c_double(a), c_double(b), c_double(c)
        )

    def angles(self):
        '''Get the three angles of an ``UnitCell``, in degrees.'''
        alpha, beta, gamma = c_double(), c_double(), c_double()
        self.c_lib.chrp_cell_angles(
            self._handle_, byref(alpha), byref(beta), byref(gamma)
        )
        return alpha.value, beta.value, gamma.value

    def set_angles(self, alpha, beta, gamma):
        '''
        Set the three angles of an ``UnitCell``, in degrees. This is only
        possible with ``TRICLINIC`` cells.
        '''
        self.c_lib.chrp_cell_set_angles(
            self._handle_, c_double(alpha), c_double(beta), c_double(gamma)
        )

    def matrix(self):
        '''Get the unit cell matricial representation.'''
        res = np.zeros((3, 3), np.float64)
        self.c_lib.chrp_cell_matrix(
            self._handle_, res
        )
        return res

    def type(self):
        '''Get the type of the unit cell'''
        res = CHRP_CELL_TYPES()
        self.c_lib.chrp_cell_type(self._handle_, byref(res))
        return CellType._from_int(res.value)

    def set_type(self, celltype):
        '''Set the type of the unit cell'''
        self.c_lib.chrp_cell_set_type(self._handle_, c_int(celltype))

    def periodicity(self):
        '''Get the cell periodic boundary conditions along the three axis'''
        x, y, z = c_bool(), c_bool(), c_bool()
        self.c_lib.chrp_cell_periodicity(
            self._handle_, byref(x), byref(y), byref(z)
        )
        return x.value, y.value, z.value

    def set_periodicity(self, x, y, z):
        '''Set the cell periodic boundary conditions along the three axis'''
        self.c_lib.chrp_cell_set_periodicity(
            self._handle_, c_bool(x), c_bool(y), c_bool(z)
        )

    def volume(self):
        '''Get the volume of the unit cell'''
        V = c_double()
        self.c_lib.chrp_cell_volume(self._handle_, byref(V))
        return V.value
