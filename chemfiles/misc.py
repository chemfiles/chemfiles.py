# -*- coding=utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals
import warnings
import sys

import ctypes
from ctypes import util
from ctypes import c_uint64, POINTER

from .clib import _get_c_library


class ChemfilesWarning(UserWarning):
    """Warnings from the Chemfiles runtime."""

    pass


class ChemfilesError(BaseException):
    """Exception class for errors in chemfiles"""

    pass


class FormatMetadata:
    """
    :py:class:`FormatMetadata` contains metadata associated with one format.
    The following fields are directly accessible:

    :param str name: name of the format
    :param str extension: extension associated with the format, or ``None`` if
                          there is no extension associated with this format
    :param str description: extended user-facing description of the format
    :param str reference: extended user-facing description of the format

    :param bool read: is reading files in this format implemented?
    :param bool write: is writing files in this format implemented?
    :param bool memory: does this format support in-memory IO?

    :param bool positions: does this format support storing atomic positions?
    :param bool velocities: does this format support storing atomic velocities?
    :param bool unit_cell: does this format support storing unit cell information?
    :param bool atoms: does this format support storing atom names or types?
    :param bool bonds: does this format support storing bonds between atoms?
    :param bool residues: does this format support storing residues?
    """

    def __init__(self):
        self.name = ""
        self.extension = None
        self.description = ""
        self.reference = ""

        self.read = False
        self.write = False
        self.memory = False

        self.positions = False
        self.velocities = False
        self.unit_cell = False
        self.atoms = False
        self.bonds = False
        self.residues = False

    def _set_from_c(self, c_format_metadata):
        self.name = c_format_metadata.name.decode("utf8")

        if c_format_metadata.extension is None:
            self.extension = None
        else:
            self.extension = c_format_metadata.extension.decode("utf8")

        self.description = c_format_metadata.description.decode("utf8")
        self.reference = c_format_metadata.reference.decode("utf8")

        self.read = c_format_metadata.read
        self.write = c_format_metadata.write
        self.memory = c_format_metadata.memory

        self.positions = c_format_metadata.positions
        self.velocities = c_format_metadata.velocities
        self.unit_cell = c_format_metadata.unit_cell
        self.atoms = c_format_metadata.atoms
        self.bonds = c_format_metadata.bonds
        self.residues = c_format_metadata.residues

    def __repr__(self):
        return """
FormatMetadata for {name}
-------------------{name_underline}
{description}

name      = {name}
extension = {extension}
reference = {reference}

Capacities:
-----------

read        = {read}
write       = {write}
memory      = {memory}
positions   = {positions}
velocities  = {velocities}
unit_cell   = {unit_cell}
atoms       = {atoms}
bonds       = {bonds}
residues    = {residues}
""".format(
            name=self.name,
            name_underline="-" * len(self.name),
            description=self.description,
            extension=self.extension,
            reference=self.reference,
            read=self.read,
            write=self.write,
            memory=self.memory,
            positions=self.positions,
            velocities=self.velocities,
            unit_cell=self.unit_cell,
            atoms=self.atoms,
            bonds=self.bonds,
            residues=self.residues,
        )


def formats_list():
    """
    Get the list of formats known by chemfiles, as well as all associated
    metadata.

    :rtype: list(FormatMetadata)
    """
    from .ffi import chfl_format_metadata

    lib = _get_c_library()

    array = POINTER(chfl_format_metadata)()
    count = c_uint64()
    lib.chfl_formats_list(array, count)

    formats = [FormatMetadata() for i in range(count.value)]
    for i in range(count.value):
        formats[i]._set_from_c(array[i])
    lib.chfl_free(array)

    return formats


# Store a reference to the last logging callback, to preven Python from
# garbage-collecting it.
_CURRENT_CALLBACK = None


def set_warnings_callback(function):
    """
    Call `function` on every warning event. The callback should take a string
    message and return nothing.

    By default, warnings are send to python `warnings` module.
    """
    from .ffi import chfl_warning_callback

    def callback(message):
        try:
            function(message.decode("utf8"))
        except Exception as e:
            message = "exception raised in warning callback: {}".format(e)
            warnings.warn(message, ChemfilesWarning)

    global _CURRENT_CALLBACK
    _CURRENT_CALLBACK = chfl_warning_callback(callback)

    _get_c_library().chfl_set_warning_callback(_CURRENT_CALLBACK)


def add_configuration(path):
    """
    Read configuration data from the file at ``path``.

    By default, chemfiles reads configuration from any file name `.chemfilesrc`
    in the current directory or any parent directory. This function can be used
    to add data from another configuration file.

    This function will fail if there is no file at ``path``, or if the file is
    incorrectly formatted. Data from the new configuration file will overwrite
    any existing data.
    """
    _get_c_library().chfl_add_configuration(path.encode("utf8"))


def _last_error():
    """Get the last error from the chemfiles runtime."""
    return _get_c_library().chfl_last_error().decode("utf8")


def _clear_errors():
    """Clear any error message saved in the chemfiles runtime."""
    return _get_c_library().chfl_clear_errors()


def _set_default_warning_callback():
    set_warnings_callback(
        # We need to set stacklevel=4 to get through the lambda =>
        # adaptor => C++ code => Python binding => user code
        lambda message: warnings.warn(message, ChemfilesWarning, stacklevel=4)
    )
