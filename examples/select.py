# This file is an example for the chemfiles library
# Any copyright is dedicated to the Public Domain.
# http://creativecommons.org/publicdomain/zero/1.0/
from chemfiles import Selection, Trajectory

trajectory = Trajectory("input.arc")
output = Trajectory("output.pdb", "w")

selection = Selection("name Zn or name N")

for frame in trajectory:
    to_remove = selection.evaluate(frame)
    for i in sorted(to_remove, reverse=True):
        frame.remove(i)
    output.write(frame)

trajectory.close()
output.close()
