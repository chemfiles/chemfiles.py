# -*- coding=utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from ctypes import c_uint64, create_string_buffer
import numpy as np

from chemfiles.types import CxxPointer
from chemfiles.ffi import chfl_match_t


class Selection(CxxPointer):
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
        ptr = self.ffi.chfl_selection(selection.encode("utf8"))
        super(Selection, self).__init__(ptr)

    def __del__(self):
        if hasattr(self, 'ptr'):
            self.ffi.chfl_selection_free(self)

    def __copy__(self):
        return Selection.from_ptr(self.ffi.chfl_selection_copy(self))

    def size(self):
        '''
        Get the size of the :py:class:`Selection`, i.e. the number of atoms we
        are selecting together.

        This value is 1 for the 'atom' context, 2 for the 'pair' and 'bond'
        context, 3 for the 'three' and 'angles' contextes and 4 for the 'four'
        and 'dihedral' contextes.
        '''
        size = c_uint64()
        self.ffi.chfl_selection_size(self, size)
        return size.value

    def string(self):
        '''
        Get the selection string used to create the :py:class:`Selection`
        '''
        selection = create_string_buffer(10)
        self.ffi.chfl_selection_string(self, selection, 10)
        return selection.value.decode("utf8")

    def evaluate(self, frame):
        '''
        Evaluate a :py:class:`Selection` for a given :py:class:`Frame`, and
        return a list of matching atoms, either a a list of index or a list
        of tuples of indexes.
        '''
        matching = c_uint64()
        self.ffi.chfl_selection_evalutate(self, frame, matching)

        matches = np.zeros(matching.value, chfl_match_t)
        self.ffi.chfl_selection_matches(self, matches, matching)

        size = self.size()
        result = []
        for match in matches:
            assert(match[0] == size)
            atoms = match[1]
            if size == 1:
                result.append(atoms[0])
            elif size == 2:
                result.append((atoms[0], atoms[1]))
            elif size == 3:
                result.append((atoms[0], atoms[1], atoms[2]))
            elif size == 4:
                result.append((atoms[0], atoms[1], atoms[2], atoms[3]))
        return result
