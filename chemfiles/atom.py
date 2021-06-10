# -*- coding=utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals
from ctypes import c_double, c_uint64, c_char_p

from typing import Optional, List, NoReturn

from .utils import CxxPointer, _call_with_growing_buffer, string_type
from .misc import ChemfilesError
from .property import Property, PropertyValueGet, PropertyValueSet


class Atom(CxxPointer):
    """
    An :py:class:`Atom` is a particle in the current :py:class:`Frame`. It
    stores the following atomic properties:

    - atom name;
    - atom type;
    - atom mass;
    - atom charge.

    The atom name is usually an unique identifier (``"H1"``, ``"C_a"``) while
    the atom type will be shared between all particles of the same type:
    ``"H"``, ``"Ow"``, ``"CH3"``.
    """

    def __init__(self, name, type=None):
        # type: (str, Optional[str]) -> None
        """
        Create a new :py:class:`Atom` with the given ``name``. If ``type`` is
        present, use it as the atom type. Else the atom name is used as atom
        type.
        """
        ptr = self.ffi.chfl_atom(name.encode("utf8"))
        super(Atom, self).__init__(ptr, is_const=False)
        if type:
            self.type = type

    def __copy__(self):
        # type: () -> Atom
        return Atom.from_mutable_ptr(None, self.ffi.chfl_atom_copy(self.ptr))

    def __repr__(self):
        # type: () -> str
        name = self.name
        type = self.type
        if type == name:
            return "Atom('{}')".format(name)
        else:
            return "Atom('{}', '{}')".format(name, type)

    @property
    def mass(self):
        # type: () -> float
        """Get this :py:class:`Atom` mass, in atomic mass units."""
        mass = c_double()
        self.ffi.chfl_atom_mass(self.ptr, mass)
        return mass.value

    @mass.setter
    def mass(self, mass):
        # type: (float) -> None
        """Set this :py:class:`Atom` mass, in atomic mass units."""
        self.ffi.chfl_atom_set_mass(self.mut_ptr, c_double(mass))

    @property
    def charge(self):
        # type: () -> float
        """
        Get this :py:class:`Atom` charge, in number of the electron charge *e*.
        """
        charge = c_double()
        self.ffi.chfl_atom_charge(self.ptr, charge)
        return charge.value

    @charge.setter
    def charge(self, charge):
        # type: (float) -> None
        """
        Set this :py:class:`Atom` charge, in number of the electron charge *e*.
        """
        self.ffi.chfl_atom_set_charge(self.mut_ptr, c_double(charge))

    @property
    def name(self):
        # type: () -> str
        """Get this :py:class:`Atom` name."""
        return _call_with_growing_buffer(
            lambda buffer, size: self.ffi.chfl_atom_name(self.ptr, buffer, size),
            initial=32,
        )

    @name.setter
    def name(self, name):
        # type: (str) -> None
        """Set this :py:class:`Atom` name to ``name``."""
        self.ffi.chfl_atom_set_name(self.mut_ptr, name.encode("utf8"))

    @property
    def type(self):
        # type: () -> str
        """Get this :py:class:`Atom` type."""
        return _call_with_growing_buffer(
            lambda buffer, size: self.ffi.chfl_atom_type(self.ptr, buffer, size),
            initial=32,
        )

    @type.setter
    def type(self, type):
        # type: (str) -> None
        """Set this :py:class:`Atom` type to ``type``."""
        self.ffi.chfl_atom_set_type(self.mut_ptr, type.encode("utf8"))

    @property
    def full_name(self):
        # type: () -> str
        """
        Try to get the full name of this :py:class:`Atom` from its type. For
        example, the full name of "He" is "Helium". If the name can not be
        found, returns the empty string.
        """
        return _call_with_growing_buffer(
            lambda buffer, size: self.ffi.chfl_atom_full_name(self.ptr, buffer, size),
            initial=64,
        )

    @property
    def vdw_radius(self):
        # type: () -> float
        """
        Try to get the Van der Waals radius of this :py:class:`Atom` from its
        type. If the radius can not be found, returns 0.
        """
        radius = c_double()
        self.ffi.chfl_atom_vdw_radius(self.ptr, radius)
        return radius.value

    @property
    def covalent_radius(self):
        # type: () -> float
        """
        Try to get the covalent radius of this :py:class:`Atom` from its type.
        If the radius can not be found, returns 0.
        """
        radius = c_double()
        self.ffi.chfl_atom_covalent_radius(self.ptr, radius)
        return radius.value

    @property
    def atomic_number(self):
        # type: () -> int
        """
        Try to get the atomic number of this :py:class:`Atom` from its type. If
        the atomic number can not be found, returns 0.
        """
        number = c_uint64()
        self.ffi.chfl_atom_atomic_number(self.ptr, number)
        return number.value

    def __iter__(self):
        # type: () -> NoReturn
        # Disable automatic iteration from __getitem__
        raise TypeError("can not iterate over an atom")

    def __getitem__(self, name):
        # type: (str) -> PropertyValueGet
        """
        Get a property of this atom with the given ``name``, or raise an error
        if the property does not exists.
        """
        if not isinstance(name, string_type):
            raise ChemfilesError(
                "Invalid type {} for an atomic property name".format(type(name))
            )
        ptr = self.ffi.chfl_atom_get_property(self.ptr, name.encode("utf8"))
        return Property.from_mutable_ptr(self, ptr).get()

    def __setitem__(self, name, value):
        # type: (str, PropertyValueSet) -> None
        """
        Set a property of this atom, with the given ``name`` and ``value``.
        The new value overwrite any pre-existing property with the same name.
        """
        if not isinstance(name, string_type):
            raise ChemfilesError(
                "invalid type {} for a property name".format(type(name))
            )
        property = Property(value)
        self.ffi.chfl_atom_set_property(self.mut_ptr, name.encode("utf8"), property.ptr)

    def properties_count(self):
        # type: () -> int
        """Get the number of properties in this atom."""
        count = c_uint64()
        self.ffi.chfl_atom_properties_count(self.ptr, count)
        return count.value

    def list_properties(self):
        # type: () -> List[str]
        """Get the name of all properties in this atom."""
        count = self.properties_count()
        StringArray = c_char_p * count
        c_names = StringArray()
        self.ffi.chfl_atom_list_properties(self.ptr, c_names, count)

        names = []
        for name in c_names:
            assert name is not None
            names.append(name.decode("utf8"))
        return names
