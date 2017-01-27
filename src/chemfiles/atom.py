# -*- coding=utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals
from ctypes import c_float, c_double, c_int, byref, create_string_buffer
from enum import IntEnum

from chemfiles import get_c_library
from chemfiles.ffi import CHFL_ATOM_TYPES
from chemfiles.errors import _check_handle


class AtomType(IntEnum):
    '''
    Available types of atoms:

    - ``AtomType.Element``: Element from the periodic table of elements
    - ``AtomType.CorseGrain``: Corse-grained atom are composed of more than one
        element: CH3 groups, amino-acids are corse-grained atoms.
    - ``AtomType.Dummy``: Dummy site, with no physical reality
    - ``AtomType.Undefined``: Undefined atom type
    '''
    Element = CHFL_ATOM_TYPES.CHFL_ATOM_ELEMENT
    CoarseGrained = CHFL_ATOM_TYPES.CHFL_ATOM_COARSE_GRAINED
    Dummy = CHFL_ATOM_TYPES.CHFL_ATOM_DUMMY
    Undefined = CHFL_ATOM_TYPES.CHFL_ATOM_UNDEFINED


class Atom(object):
    '''
    An :py:class:`Atom` is a particle in the current :py:class:`Frame`. It can
    be used to store and retrieve informations about a particle, such as mass,
    name, atomic number, *etc.*
    '''

    def __init__(self, name):
        '''Create a new :py:class:`Atom` from a ``name``.'''
        self.c_lib = get_c_library()
        self._handle_ = self.c_lib.chfl_atom(name.encode("utf8"))
        _check_handle(self._handle_)

    def __del__(self):
        self.c_lib.chfl_atom_free(self._handle_)

    def mass(self):
        '''Get the :py:class:`Atom` mass, in atomic mass units'''
        res = c_float()
        self.c_lib.chfl_atom_mass(self._handle_, byref(res))
        return res.value

    def set_mass(self, mass):
        '''Set the :py:class:`Atom` mass, in atomic mass units'''
        self.c_lib.chfl_atom_set_mass(self._handle_, c_float(mass))

    def charge(self):
        '''
        Get the :py:class:`Atom` charge, in number of the electron charge *e*
        '''
        res = c_float()
        self.c_lib.chfl_atom_charge(self._handle_, byref(res))
        return res.value

    def set_charge(self, charge):
        '''
        Set the :py:class:`Atom` charge, in number of the electron charge *e*
        '''
        self.c_lib.chfl_atom_set_charge(self._handle_, c_float(charge))

    def name(self):
        '''Get the :py:class:`Atom` name'''
        res = create_string_buffer(10)
        self.c_lib.chfl_atom_name(self._handle_, res, 10)
        return res.value.decode("utf8")

    def set_name(self, name):
        '''Set the :py:class:`Atom` name'''
        self.c_lib.chfl_atom_set_name(self._handle_, name.encode("utf8"))

    def full_name(self):
        '''
        Try to get the full name of the :py:class:`Atom`. The full name of "He"
        is "Helium", and so on. If the name can not be found, returns the empty
        string.
        '''
        res = create_string_buffer(100)
        self.c_lib.chfl_atom_full_name(self._handle_, res, 100)
        return res.value.decode("utf8")

    def vdw_radius(self):
        '''
        Try to get the Van der Waals radius of the :py:class:`Atom`. If the
        radius can not be found, returns -1.
        '''
        res = c_double()
        self.c_lib.chfl_atom_vdw_radius(self._handle_, byref(res))
        return res.value

    def covalent_radius(self):
        '''
        Try to get the covalent radius of the :py:class:`Atom`. If the radius
        can not be found, returns -1.
        '''
        res = c_double()
        self.c_lib.chfl_atom_covalent_radius(self._handle_, byref(res))
        return res.value

    def atomic_number(self):
        '''
        Try to get the atomic number of the :py:class:`Atom`. If the number can
        not be found, returns -1.
        '''
        res = c_int()
        self.c_lib.chfl_atom_atomic_number(self._handle_, byref(res))
        return res.value

    def type(self):
        '''Get the type of the atom'''
        res = CHFL_ATOM_TYPES()
        self.c_lib.chfl_atom_type(self._handle_, byref(res))
        return AtomType(res.value)

    def set_type(self, atomtype):
        '''Set the type of the atom'''
        self.c_lib.chfl_atom_set_type(self._handle_, c_int(atomtype))
