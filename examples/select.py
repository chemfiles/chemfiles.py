# This file is an example for the chemfiles library
# Any copyright is dedicated to the Public Domain.
# http://creativecommons.org/publicdomain/zero/1.0/
#!/usr/bin/env python
from chemfiles import Trajectory, Selection

trajectory = Trajectory("input.arc")
output = Trajectory("output.pdb", "w")

selection = Selection("name Zn or name N")

for frame in trajectory:
    to_remove = selection.evaluate(frame)
    for i in reversed(sorted(to_remove)):
        frame.remove(i)
    output.write(frame)

trajectory.close()
output.close()
