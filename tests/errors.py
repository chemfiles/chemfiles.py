# -*- coding=utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals
import unittest

import chemfiles
from chemfiles import Trajectory, ChemfilesException


class TestErrors(unittest.TestCase):
    def test_last_error(self):
        self.assertEqual(chemfiles.errors._last_error(), "")

        try:
            Trajectory("noextention")
        except ChemfilesException:
            pass
        self.assertEqual(
            chemfiles.errors._last_error(),
            "file at 'noextention' does not have an extension, provide a "
            "format name to read it"
        )

        chemfiles.errors._clear_errors()
        self.assertEqual(chemfiles.errors._last_error(), "")


if __name__ == '__main__':
    unittest.main()
