# -*- coding=utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals
import ctypes
from ctypes import c_uint64, c_char_p

from .utils import CxxPointer
from .frame import Frame, Topology
from .misc import ChemfilesError


class Trajectory(CxxPointer):
    """
    A :py:class:`Trajectory` is a chemistry file on the hard drive. It is the
    main entry point of Chemfiles.
    """

    def __init__(self, path, mode="r", format=""):
        """
        Open the :py:class:`Trajectory` at the given ``path`` using the
        given ``mode`` and optional specific file ``format``.

        Valid modes are ``'r'`` for read, ``'w'`` for write and ``'a'`` for
        append.

        The specific file format is needed when the file format does not match
        the extension, or when there is not standard extension for this format.
        If `format` is an empty string, the format will be guessed from the
        file extension.
        """
        self.__closed = False
        # Store mode and format for __repr__
        self.__mode = mode
        self.__format = format
        ptr = self.ffi.chfl_trajectory_with_format(
            path.encode("utf8"), mode.encode("utf8"), format.encode("utf8")
        )
        super(Trajectory, self).__init__(ptr, is_const=False)

    def __check_opened(self):
        if self.__closed:
            raise ChemfilesError("Can not use a closed Trajectory")

    def __del__(self):
        if not self.__closed:
            self.close()

    def __enter__(self):
        self.__check_opened()
        return self

    def __exit__(self, *args):
        self.close()

    def __iter__(self):
        self.__check_opened()
        for step in range(self.nsteps):
            yield self.read_step(step)

    def __repr__(self):
        return "Trajectory('{}', '{}', '{}')".format(self.path, self.__mode, self.__format)

    def read(self):
        """
        Read the next step of the :py:class:`Trajectory` and return the
        corresponding :py:class:`Frame`.
        """
        self.__check_opened()
        frame = Frame()
        self.ffi.chfl_trajectory_read(self.mut_ptr, frame.mut_ptr)
        return frame

    def read_step(self, step):
        """
        Read a specific ``step`` in the :py:class:`Trajectory` and return the
        corresponding :py:class:`Frame`.
        """
        self.__check_opened()
        frame = Frame()
        self.ffi.chfl_trajectory_read_step(self.mut_ptr, c_uint64(step), frame.mut_ptr)
        return frame

    def write(self, frame):
        """Write a :py:class:`Frame` to the :py:class:`Trajectory`."""
        self.__check_opened()
        self.ffi.chfl_trajectory_write(self.mut_ptr, frame.ptr)

    def set_topology(self, topology, format=""):
        """
        Set the :py:class:`Topology` associated with a :py:class:`Trajectory`.
        This :py:class:`Topology` will be used when reading and writing the
        files, replacing any :py:class:`Topology` in the frames or files.

        If ``topology`` is a :py:class:`Topology` instance, it is used
        directly. If ``topology`` is a string, the first :py:class:`Frame` of
        the corresponding file is read, and the topology of this frame is used.

        When reading from a file, if ``format`` is not the empty string, the
        code uses this file format instead of guessing it from the file
        extension.
        """
        self.__check_opened()
        if isinstance(topology, Topology):
            self.ffi.chfl_trajectory_set_topology(self.mut_ptr, topology.ptr)
        else:
            self.ffi.chfl_trajectory_topology_file(
                self.mut_ptr, topology.encode("utf8"), format.encode("utf8")
            )

    def set_cell(self, cell):
        """
        Set the :py:class:`UnitCell` associated with a :py:class:`Trajectory`.
        This :py:class:`UnitCell` will be used when reading and writing the
        files, replacing any :py:class:`UnitCell` in the frames or files.
        """
        self.__check_opened()
        self.ffi.chfl_trajectory_set_cell(self.mut_ptr, cell.ptr)

    @property
    def nsteps(self):
        """
        Get the number of steps (the number of frames) in a
        :py:class:`Trajectory`.
        """
        self.__check_opened()
        nsteps = c_uint64()
        self.ffi.chfl_trajectory_nsteps(self.mut_ptr, nsteps)
        return nsteps.value

    @property
    def path(self):
        """Get the path used to open this  :py:class:`Trajectory`."""
        self.__check_opened()
        path = c_char_p()
        self.ffi.chfl_trajectory_path(self.ptr, path)
        return path.value.decode('utf-8')

    def close(self):
        """
        Close the :py:class:`Trajectory` and write any buffered content to the
        hard drive.
        """
        self.__check_opened()
        self.__closed = True
        self.ffi.chfl_trajectory_close(self.ptr)
