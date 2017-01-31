# -*- coding=utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals
from ctypes import c_uint64

from chemfiles.utils import CxxPointer
from chemfiles.frame import Frame, Topology
from chemfiles.errors import ChemfilesException


class Trajectory(CxxPointer):
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
        self.closed = False
        ptr = self.ffi.chfl_trajectory_with_format(
            path.encode("utf8"), mode.encode("utf8"), format.encode("utf8")
        )
        super(Trajectory, self).__init__(ptr)

    def _check_opened(self):
        if self.closed:
            raise ChemfilesException("Can not use a closed trajectory")

    def __del__(self):
        if not self.closed and hasattr(self, 'ptr'):
            self.close()

    def __enter__(self):
        self._check_opened()
        return self

    def __exit__(self, *args):
        # The C pointer will be deleted by the call to __del__, so no need to
        # call chfl_trajectory_close ourselves.
        pass

    def __iter__(self):
        self._check_opened()
        frame = Frame()
        for _ in range(self.nsteps()):
            self.read(frame)
            yield frame

    def read(self, frame=None):
        '''
        Read the next step of the :py:class:`Trajectory` and return the
        corresponding :py:class:`Frame`. If the ``frame`` parameter is given,
        reuse the corresponding allocation.
        '''
        self._check_opened()
        if not frame:
            frame = Frame()
        self.ffi.chfl_trajectory_read(self, frame)
        return frame

    def read_step(self, step, frame=None):
        '''
        Read a specific step in the :py:class:`Trajectory` and return the
        corresponding :py:class:`Frame`. If the ``frame`` parameter is given,
        reuse the corresponding allocation.
        '''
        self._check_opened()
        if not frame:
            frame = Frame()
        self.ffi.chfl_trajectory_read_step(self, c_uint64(step), frame)
        return frame

    def write(self, frame):
        '''Write a :py:class:`Frame` to the :py:class:`Trajectory`'''
        self._check_opened()
        self.ffi.chfl_trajectory_write(self, frame)

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
        self._check_opened()
        if isinstance(topology, Topology):
            self.ffi.chfl_trajectory_set_topology(self, topology)
        else:
            self.ffi.chfl_trajectory_set_topology_with_format(
                self, topology.encode("utf8"), format.encode("utf8")
            )

    def set_cell(self, cell):
        '''
        Set the :py:class:`UnitCell` associated with a :py:class:`Trajectory`.
        This :py:class:`UnitCell` will be used when reading and writing the
        files, replacing any :py:class:`UnitCell` in the frames or files.
        '''
        self._check_opened()
        self.ffi.chfl_trajectory_set_cell(self, cell)

    def nsteps(self):
        '''
        Get the number of steps (the number of frames) in a
        :py:class:`Trajectory`.
        '''
        self._check_opened()
        nsteps = c_uint64()
        self.ffi.chfl_trajectory_nsteps(self, nsteps)
        return nsteps.value

    def close(self):
        '''
        Close the :py:class:`Trajectory` and write any buffered content to the
        hard drive.
        '''
        self._check_opened()
        self.closed = True
        self.ffi.chfl_trajectory_close(self)
