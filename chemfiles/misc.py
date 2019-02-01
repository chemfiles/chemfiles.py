# -*- coding=utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals
import warnings

from .clib import _get_c_library


class ChemfilesWarning(UserWarning):
    """Warnings from the Chemfiles runtime."""

    pass


class ChemfilesError(BaseException):
    """Exception class for errors in chemfiles"""

    pass


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
    incorectly formatted. Data from the new configuration file will overwrite
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
        # adapatator => C++ code => Python binding => user code
        lambda message: warnings.warn(message, ChemfilesWarning, stacklevel=4)
    )
