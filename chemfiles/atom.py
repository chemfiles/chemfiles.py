# -*- coding=utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals
from ctypes import c_double, c_uint64

from .utils import CxxPointer, _call_with_growing_buffer
from .property import Property


class Atom(CxxPointer):
    '''
    An :py:class:`Atom` is a particle in the current :py:class:`Frame`. It
    stores the following atomic properties:

    - atom name;
    - atom type;
    - atom mass;
    - atom charge.

    The atom name is usually an unique identifier (``"H1"``, ``"C_a"``) while
    the atom type will be shared between all particles of the same type:
    ``"H"``, ``"Ow"``, ``"CH3"``.
    '''

    def __init__(self, name, type=None):
        '''
        Create a new :py:class:`Atom` from a ``name``, and set the atom type
        to ``name``.
        '''
        super(Atom, self).__init__(self.ffi.chfl_atom(name.encode("utf8")))
        if type:
            self.set_type(type)

    def __del__(self):
        if hasattr(self, 'ptr'):
            self.ffi.chfl_atom_free(self)

    def __copy__(self):
        return Atom.from_ptr(self.ffi.chfl_atom_copy(self))

    def mass(self):
        '''Get this :py:class:`Atom` mass, in atomic mass units.'''
        mass = c_double()
        self.ffi.chfl_atom_mass(self, mass)
        return mass.value

    def set_mass(self, mass):
        '''Set this :py:class:`Atom` mass, in atomic mass units.'''
        self.ffi.chfl_atom_set_mass(self, c_double(mass))

    def charge(self):
        '''
        Get this :py:class:`Atom` charge, in number of the electron charge *e*.
        '''
        charge = c_double()
        self.ffi.chfl_atom_charge(self, charge)
        return charge.value

    def set_charge(self, charge):
        '''
        Set this :py:class:`Atom` charge, in number of the electron charge *e*.
        '''
        self.ffi.chfl_atom_set_charge(self, c_double(charge))

    def name(self):
        '''Get this :py:class:`Atom` name.'''
        return _call_with_growing_buffer(
            lambda buffer, size: self.ffi.chfl_atom_name(self, buffer, size),
            initial=32,
        )

    def set_name(self, name):
        '''Set this :py:class:`Atom` name to ``name``.'''
        self.ffi.chfl_atom_set_name(self, name.encode("utf8"))

    def type(self):
        '''Get this :py:class:`Atom` type.'''
        return _call_with_growing_buffer(
            lambda buffer, size: self.ffi.chfl_atom_type(self, buffer, size),
            initial=32,
        )

    def set_type(self, type):
        '''Set this :py:class:`Atom` type to ``type``.'''
        self.ffi.chfl_atom_set_type(self, type.encode("utf8"))

    def full_name(self):
        '''
        Try to get the full name of this :py:class:`Atom` from its type. For
        example, the full name of "He" is "Helium". If the name can not be
        found, returns the empty string.
        '''
        return _call_with_growing_buffer(
            lambda buff, size: self.ffi.chfl_atom_full_name(self, buff, size),
            initial=64,
        )

    def vdw_radius(self):
        '''
        Try to get the Van der Waals radius of this :py:class:`Atom` from its
        type. If the radius can not be found, returns 0.
        '''
        radius = c_double()
        self.ffi.chfl_atom_vdw_radius(self, radius)
        return radius.value

    def covalent_radius(self):
        '''
        Try to get the covalent radius of this :py:class:`Atom` from its type.
        If the radius can not be found, returns 0.
        '''
        radius = c_double()
        self.ffi.chfl_atom_covalent_radius(self, radius)
        return radius.value

    def atomic_number(self):
        '''
        Try to get the atomic number of this :py:class:`Atom` from its type. If
        the atomic number can not be found, returns 0.
        '''
        number = c_uint64()
        self.ffi.chfl_atom_atomic_number(self, number)
        return number.value

    def set(self, name, value):
        '''
        Set a property of this atom, with the given ``name`` and ``value``.
        The new value overwrite any pre-existing property with the same name.
        '''
        self.ffi.chfl_atom_set_property(
            self, name.encode("utf8"), Property(value)
        )

    def get(self, name):
        '''
        Get a property of this atom with the given ``name``, or raise an error
        if the property does not exists.
        '''
        ptr = self.ffi.chfl_atom_get_property(self, name.encode("utf8"))
        return Property.from_ptr(ptr).get()
