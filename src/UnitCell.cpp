/*
 * Chemharp, an efficient IO library for chemistry file formats
 * Copyright (C) 2015 Guillaume Fraux
 *
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/
*/

#include "chemharp-python.hpp"

void register_unit_cell() {
    /* UnitCell class *********************************************************/
    py::class_<UnitCell>("UnitCell", py::init<>())
        .def(py::init<double>())
        .def(py::init<double, double, double>())
        .def(py::init<double, double, double, double, double, double>())
        .def(py::init<UnitCell::CellType>())
        .def(py::init<UnitCell::CellType, double>())
        .def(py::init<UnitCell::CellType, double, double, double>())
        .def("matricial", &UnitCell::matricial, py::return_value_policy<Matrix3D_convertor>())

        .def("type", static_cast<UnitCell::CellType (UnitCell::*)(void) const>(&UnitCell::type))
        .def("type", static_cast<void (UnitCell::*)(UnitCell::CellType)>(&UnitCell::type))

        .def("a", static_cast<double (UnitCell::*)(void) const>(&UnitCell::a))
        .def("a", static_cast<void (UnitCell::*)(double)>(&UnitCell::a))

        .def("b", static_cast<double (UnitCell::*)(void) const>(&UnitCell::b))
        .def("b", static_cast<void (UnitCell::*)(double)>(&UnitCell::b))

        .def("c", static_cast<double (UnitCell::*)(void) const>(&UnitCell::c))
        .def("c",static_cast<void (UnitCell::*)(double)>(&UnitCell::c))

        .def("alpha", static_cast<double (UnitCell::*)(void) const>(&UnitCell::alpha))
        .def("alpha", static_cast<void (UnitCell::*)(double)>(&UnitCell::alpha))

        .def("beta", static_cast<double (UnitCell::*)(void) const>(&UnitCell::beta))
        .def("beta", static_cast<void (UnitCell::*)(double)>(&UnitCell::beta))

        .def("gamma", static_cast<double (UnitCell::*)(void) const>(&UnitCell::gamma))
        .def("gamma", static_cast<void (UnitCell::*)(double)>(&UnitCell::gamma))

        .def("volume", static_cast<double (UnitCell::*)(void) const>(&UnitCell::volume))

        .def("periodic_x", static_cast<bool (UnitCell::*)(void) const>(&UnitCell::periodic_x))
        .def("periodic_x", static_cast<void (UnitCell::*)(bool)>(&UnitCell::periodic_x))

        .def("periodic_y", static_cast<bool (UnitCell::*)(void) const>(&UnitCell::periodic_y))
        .def("periodic_y", static_cast<void (UnitCell::*)(bool)>(&UnitCell::periodic_y))

        .def("periodic_z", static_cast<bool (UnitCell::*)(void) const>(&UnitCell::periodic_z))
        .def("periodic_z", static_cast<void (UnitCell::*)(bool)>(&UnitCell::periodic_z))

        .def("full_periodic", static_cast<bool (UnitCell::*)(void) const>(&UnitCell::full_periodic))
        .def("full_periodic", static_cast<void (UnitCell::*)(bool)>(&UnitCell::full_periodic))
    ;

    /* CellType enum **********************************************************/
    py::enum_<UnitCell::CellType>("CellType")
        .value("ORTHOROMBIC", UnitCell::ORTHOROMBIC)
        .value("TRICLINIC", UnitCell::TRICLINIC)
        .value("INFINITE", UnitCell::INFINITE)
    ;
}
