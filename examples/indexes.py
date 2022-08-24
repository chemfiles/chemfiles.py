# This trajectory is an example for the chemfiles library
# Any copyright is dedicated to the Public Domain.
# http://creativecommons.org/publicdomain/zero/1.0/
#!/usr/bin/env python
from chemfiles import Trajectory

with Trajectory("filename.xyz") as trajectory:
    frame = trajectory.read()

less_than_five = []
for i in range(len(frame.atoms)):
    if frame.positions[i, 0] < 5:
        less_than_five.append(i)

print("Atoms with x < 5: ")
for i in less_than_five:
    print(f"  - {i}")
