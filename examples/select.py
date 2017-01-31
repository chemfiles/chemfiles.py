# File indexes.py, example for the Chemharp library
# Any copyright is dedicated to the Public Domain.
# http://creativecommons.org/publicdomain/zero/1.0/

#!/usr/bin/env python
# -*- coding: utf-8 -*-

from chemfiles import Trajectory, Selection

# Read a frame from a given file
frame = Trajectory("filename.xyz").read()


# Create a selection for all atoms with "Zn" name
selection = Selection("name Zn")
# Get the list of matching atoms from the frame
zincs = selection.evaluate(frame)

print("We have {} zinc in the frame".format(len(zincs)))
for i in zincs:
    print("{} is a zinc".format(i))


# Create a selection for multiple atoms
selection = Selection("angles: name(#1) H and name(#2) O and name(#3) H")
# Get the list of matching atoms in the frame
waters = selection.evaluate(frame)

print("We have {} water molecules".format(len(waters)))
for (i, j, k) in waters:
    print("{} - {} - {} is a water".format(i, j, k))
