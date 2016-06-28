# File convert.py, example for the chemfiles library
# Any copyright is dedicated to the Public Domain.
# http://creativecommons.org/publicdomain/zero/1.0/

#!/usr/bin/env python
# -*- coding: utf-8 -*-

from chemfiles import Trajectory, UnitCell, Atom, Topology

infile = Trajectory("water.xyz")

# Orthorombic UnitCell with lengths of 20, 15 and 35 A
cell = UnitCell(20, 15, 35)
infile.set_cell(cell)

# Create Atoms
O = Atom("O")
H = Atom("H")

# Create topology with one water molecule
topology = Topology()
topology.append(O)
topology.append(H)
topology.append(H)

topology.add_bond(0, 1)
topology.add_bond(0, 2)
infile.set_topology(topology)

# Write an output file using PDB format
output = Trajectory("water.pdb", "w")

for _ in range(infile.nsteps()):
    frame = infile.read()
    output.write(frame)
