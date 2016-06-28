# File indexes.py, example for the chemfiles library
# Any copyright is dedicated to the Public Domain.
# http://creativecommons.org/publicdomain/zero/1.0/

#!/usr/bin/env python
# -*- coding: utf-8 -*-

from chemfiles import Trajectory

trajectory = Trajectory("filename.xyz")
frame = trajectory.read()
positions = frame.positions()

indexes = []
for i in range(frame.natoms()):
    # positions is a numpy ndarray
    if positions[i, 0] < 5:
        indexes.append(i)

print("Atoms with x < 5:")
for i in indexes:
    print("  - {}".format(i))
