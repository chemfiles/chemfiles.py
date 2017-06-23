# -*- coding=utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals
import unittest
import os

from chemfiles import misc, add_configuration
from chemfiles import Trajectory, ChemfilesException


class TestMisc(unittest.TestCase):
    def test_last_error(self):
        self.assertEqual(misc._last_error(), "")

        try:
            Trajectory("noextention")
        except ChemfilesException:
            pass
        self.assertEqual(
            misc._last_error(),
            "Can not find a format associated with the \"\" extension."
        )

        misc._clear_errors()
        self.assertEqual(misc._last_error(), "")

    def test_configuration(self):
        with open("tmp-config.toml", "w") as fd:
            fd.write("""
            [types]
            O = "replaced"
            """)

        add_configuration("tmp-config.toml")

        frame = Trajectory(os.path.join("data", "water.xyz")).read()
        topology = frame.topology()
        self.assertEqual(topology.atom(0).name(), "O")
        self.assertEqual(topology.atom(0).type(), "replaced")

        os.unlink("tmp-config.toml")


if __name__ == '__main__':
    unittest.main()
