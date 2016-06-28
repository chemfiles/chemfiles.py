# File rmsd.py, example for the chemfiles library
# Any copyright is dedicated to the Public Domain.
# http://creativecommons.org/publicdomain/zero/1.0/

#!/usr/bin/env python
# -*- coding: utf-8 -*-

from chemfiles import Trajectory
import math

trajectory = Trajectory("filename.nc")
distances = []
# Accumulate the distances to the origin of the 10th atom throughtout the
# trajectory
for _ in range(trajectory.nsteps()):
    frame = trajectory.read()
    # Position of the 10th atom
    position = frame.positions()[9, :]
    distance = math.sqrt(position.dot(position))
    distances.append(distance)

mean = sum(distances) / len(distances)
rmsd = 0.0
for dist in distances:
    rmsd += (mean - dist) * (mean - dist)

rmsd /= len(distances)
rmsd = math.sqrt(rmsd)

print("Root-mean square displacement is: {}".format(rmsd))
