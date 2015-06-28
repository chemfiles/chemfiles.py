/*
 * Chemharp, an efficient IO library for chemistry file formats
 * Copyright (C) 2015 Guillaume Fraux
 *
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/
*/

#include "chemharp-python.hpp"

void register_atom() {
    /* Atom class *************************************************************/
    py::scope atom_scope = py::class_<Atom>("Atom", py::init<string>())
        .def("name", py::make_function(
            static_cast<const string& (Atom::*)(void) const>(&Atom::name),
            py::return_value_policy<py::copy_const_reference>()))
        .def("name", static_cast<void (Atom::*)(const string&)>(&Atom::name))
        .def("mass", py::make_function(
            static_cast<const float& (Atom::*)(void) const>(&Atom::mass),
            py::return_value_policy<py::copy_const_reference>()))
        .def("mass", static_cast<void (Atom::*)(float)>(&Atom::mass))
        .def("charge", py::make_function(
            static_cast<const float& (Atom::*)(void) const>(&Atom::charge),
            py::return_value_policy<py::copy_const_reference>()))
        .def("charge", static_cast<void (Atom::*)(float)>(&Atom::charge))
        .def("type", py::make_function(
            static_cast<const Atom::AtomType& (Atom::*)(void) const>(&Atom::type),
            py::return_value_policy<py::copy_const_reference>()))
        .def("type", static_cast<void (Atom::*)(Atom::AtomType)>(&Atom::type))
        .def("full_name", &Atom::full_name)
        .def("vdw_radius", &Atom::vdw_radius)
        .def("covalent_radius", &Atom::covalent_radius)
        .def("atomic_number", &Atom::atomic_number)
        .def("__cmp__", &Atom::operator==)
    ;

    /* AtomType enum **********************************************************/
    py::enum_<Atom::AtomType>("AtomType")
        .value("ELEMENT", Atom::ELEMENT)
        .value("CORSE_GRAIN", Atom::CORSE_GRAIN)
        .value("DUMMY", Atom::DUMMY)
        .value("UNDEFINED", Atom::UNDEFINED)
    ;
}
