# This file is an example for the chemfiles library
# Any copyright is dedicated to the Public Domain.
# http://creativecommons.org/publicdomain/zero/1.0/
#!/usr/bin/env python
import numpy as np
from chemfiles import Topology, Frame, Atom, UnitCell, Trajectory

topology = Topology()
topology.atoms.append(Atom("H"))
topology.atoms.append(Atom("O"))
topology.atoms.append(Atom("H"))

topology.add_bond(0, 1)
topology.add_bond(2, 1)

frame = Frame()
frame.resize(3)
frame.topology = topology

frame.positions[0, :] = np.array([1.0, 0.0, 0.0])
frame.positions[1, :] = np.array([0.0, 0.0, 0.0])
frame.positions[2, :] = np.array([0.0, 1.0, 0.0])

frame.add_atom(Atom("O"), [5.0, 0.0, 0.0])
frame.add_atom(Atom("C"), [6.0, 0.0, 0.0])
frame.add_atom(Atom("O"), [7.0, 0.0, 0.0])
frame.add_bond(3, 4)
frame.add_bond(4, 5)

frame.cell = UnitCell(10, 10, 10)

with Trajectory("water-co2.pdb", 'w') as trajectory:
    trajectory.write(frame)
