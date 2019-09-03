# -*- coding=utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals
import unittest
import tempfile
import shutil
import os

from chemfiles import Trajectory, Frame, Atom

ROOT = os.path.dirname(__file__)


class TestExamples(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._cwd = os.getcwd()
        cls._tmpdir = tempfile.mkdtemp()
        os.chdir(cls._tmpdir)

    @classmethod
    def tearDownClass(cls):
        os.chdir(cls._cwd)
        shutil.rmtree(cls._tmpdir)

    def test_generate(self):
        path = os.path.join(ROOT, "..", "examples", "generate.py")
        exec(open(path).read(), globals())

    def test_indexes(self):
        # Create an input file
        frame = Frame()
        for i in range(120):
            frame.add_atom(Atom('X'), [i % 10, i + 1 % 10, i + 2 % 10])

        with Trajectory("filename.xyz", "w") as file:
            file.write(frame)

        path = os.path.join(ROOT, "..", "examples", "indexes.py")
        # disable output
        exec(open(path).read(), globals(), {'print': lambda _: None})

    def test_select(self):
        # Create an input file
        frame = Frame()
        NAMES = ["N", "Zn", "C", "O"]
        for i in range(120):
            frame.add_atom(Atom(NAMES[i % 4]), [i % 10, i + 1 % 10, i + 2 % 10])

        with Trajectory("input.arc", "w")as file:
            file.write(frame)

        path = os.path.join(ROOT, "..", "examples", "select.py")
        exec(open(path).read(), globals())


if __name__ == "__main__":
    unittest.main()
