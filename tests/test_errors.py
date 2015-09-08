# -*- coding=utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals
import unittest
import os

from chemharp import logging
from chemharp.logging import LogLevel


class TestLogging(unittest.TestCase):
    def test_level(self):
        self.assertEqual(logging.log_level(), LogLevel.ERROR)
        logging.set_log_level(LogLevel.DEBUG)
        self.assertEqual(logging.log_level(), LogLevel.DEBUG)
        logging.set_log_level(LogLevel.ERROR)

    def test_redirect(self):
        logging.log_to_file("test.log")
        self.assertTrue(os.path.isfile("test.log"))
        logging.log_to_stderr()
