# -*- coding=utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals
from ctypes import c_uint64, byref

from chemfiles import get_c_library
from chemfiles.errors import _check_handle
from chemfiles.frame import Frame, Topology


class Trajectory(object):
    '''
    A :py:class:`Trajectory` is a chemistry file on the hard drive. It is the
    main entry point of Chemfiles.
    '''

    def __init__(self, path, mode="r", format=""):
        '''
        Open a trajectory file at ``path`` with mode ``mode``. Supported modes
        are "r" for read (this is the default) or "w" for write. If ``format``
        is not the empty string, use it instead of guessing the format from the
        file extension.
        '''
        self.c_lib = get_c_library()
        self._handle_ = self.c_lib.chfl_trajectory_with_format(
            path.encode("utf8"), mode.encode("utf8"), format.encode("utf8")
        )
        _check_handle(self._handle_)

    def __del__(self):
        self.c_lib.chfl_trajectory_close(self._handle_)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        # The C pointer will be deleted by the call to __del__, so no need to
        # call chfl_trajectory_close ourselves.
        pass

    def read(self):
        '''
        Read the next step of the :py:class:`Trajectory` and return the
        corresponding :py:class:`Frame`
        '''
        frame = Frame()
        self.c_lib.chfl_trajectory_read(self._handle_, frame._handle_)
        return frame

    def read_step(self, step):
        '''
        Read a specific step in the :py:class:`Trajectory` and return the
        corresponding :py:class:`Frame`.
        '''
        frame = Frame()
        self.c_lib.chfl_trajectory_read_step(
            self._handle_, c_uint64(step), frame._handle_
        )
        return frame

    def write(self, frame):
        '''Write a :py:class:`Frame` to the :py:class:`Trajectory`'''
        self.c_lib.chfl_trajectory_write(self._handle_, frame._handle_)

    def set_topology(self, topology, format=""):
        '''
        Set the :py:class:`Topology` associated with a :py:class:`Trajectory`.
        This :py:class:`Topology` will be used when reading and writing the
        files, replacing any :py:class:`Topology` in the frames or files.

        If ``topology`` is a :py:class:`Topology` instance, it is used
        directly. If ``topology`` is a string, the first :py:class:`Frame` of
        the corresponding file is read, and the topology of this frame is used.

        When reading from a file, if ``format`` is not the empty string, the
        code uses this file format instead of guessing it from the file
        extension.
        '''

        if isinstance(topology, Topology):
            self.c_lib.chfl_trajectory_set_topology(
                self._handle_, topology._handle_
            )
        else:
            self.c_lib.chfl_trajectory_set_topology_with_format(
                self._handle_, topology.encode("utf8"), format.encode("utf8")
            )

    def set_cell(self, cell):
        '''
        Set the :py:class:`UnitCell` associated with a :py:class:`Trajectory`.
        This :py:class:`UnitCell` will be used when reading and writing the
        files, replacing any :py:class:`UnitCell` in the frames or files.
        '''
        self.c_lib.chfl_trajectory_set_cell(self._handle_, cell._handle_)

    def nsteps(self):
        '''
        Get the number of steps (the number of frames) in a
        :py:class:`Trajectory`.
        '''
        res = c_uint64()
        self.c_lib.chfl_trajectory_nsteps(self._handle_, byref(res))
        return res.value
