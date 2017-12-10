# This trajectory is an example for the chemtrajectorys library
# Any copyright is dedicated to the Public Domain.
# http://creativecommons.org/publicdomain/zero/1.0/
#!/usr/bin/env python
from chemfiles import Trajectory

trajectory = Trajectory("filename.xyz")
frame = trajectory.read()

less_than_five = []
positions = frame.positions()

for i in range(len(frame)):
    if positions[i, 0] < 5:
        less_than_five.append(i)

print("Atoms with x < 5: ")
for i in less_than_five:
    print("  - {}".format(i))
