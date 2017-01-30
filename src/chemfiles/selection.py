# -*- coding=utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from ctypes import byref, c_uint64, create_string_buffer
import numpy as np

from chemfiles import get_c_library
from chemfiles.errors import _check_handle
from chemfiles.ffi import chfl_match_t


class Selection(object):
    '''
    Select atoms in a :py:class:`Frame` with a selection language.

    The selection language is built by combining basic operations. Each basic
    operation follows the ``<selector>[(<variable>)] <operator> <value>``
    structure, where ``<operator>`` is a comparison operator in
    ``== != < <= > >=``. Refer to the `full documentation
    <selections-doc>`_ to know the allowed selectors and how to use them.

    .. selections-doc: http://chemfiles.rtfd.io/en/latest/selections.html
    '''

    def __init__(self, selection):
        '''
        Create a new :py:class:`Selection` from the given selection string.
        '''
        self.c_lib = get_c_library()
        self._handle_ = self.c_lib.chfl_selection(selection.encode("utf8"))
        _check_handle(self._handle_)

    def __del__(self):
        self.c_lib.chfl_selection_free(self._handle_)

    def __copy__(self):
        selection = self.__new__(Selection)
        selection.c_lib = get_c_library()
        selection._handle_ = self.c_lib.chfl_selection_copy(self._handle_)
        _check_handle(selection._handle_)
        return selection

    def size(self):
        '''
        Get the size of the :py:class:`Selection`, i.e. the number of atoms we
        are selecting together.

        This value is 1 for the 'atom' context, 2 for the 'pair' and 'bond'
        context, 3 for the 'three' and 'angles' contextes and 4 for the 'four'
        and 'dihedral' contextes.
        '''
        res = c_uint64()
        self.c_lib.chfl_selection_size(self._handle_, byref(res))
        return res.value

    def string(self):
        '''
        Get the selection string used to create the :py:class:`Selection`
        '''
        res = create_string_buffer(10)
        self.c_lib.chfl_selection_string(self._handle_, res, 10)
        return res.value.decode("utf8")

    def evaluate(self, frame):
        '''
        Evaluate a :py:class:`Selection` for a given :py:class:`Frame`, and
        return a list of matching atoms, either a a list of index or a list
        of tuples of indexes.
        '''
        matching = c_uint64()
        self.c_lib.chfl_selection_evalutate(
            self._handle_, frame._handle_, byref(matching)
        )

        matches = np.zeros(matching.value, chfl_match_t)
        self.c_lib.chfl_selection_matches(
            self._handle_, matches, matching
        )

        size = self.size()
        res = []
        for match in matches:
            assert(match[0] == size)
            atoms = match[1]
            if size == 1:
                res.append(atoms[0])
            elif size == 2:
                res.append((atoms[0], atoms[1]))
            elif size == 3:
                res.append((atoms[0], atoms[1], atoms[2]))
            elif size == 4:
                res.append((atoms[0], atoms[1], atoms[2], atoms[3]))
        return res
