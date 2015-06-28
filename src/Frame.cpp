/*
 * Chemharp, an efficient IO library for chemistry file formats
 * Copyright (C) 2015 Guillaume Fraux
 *
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/
*/

#include "chemharp-python.hpp"

void register_frame() {
    /* Frame class ************************************************************/
    py::class_<Frame>("Frame", py::init<py::optional<size_t>>())
        .def("positions", py::make_function(
            static_cast<const Array3D& (Frame::*)(void) const>(&Frame::positions),
            py::return_value_policy<Array3D_convertor>()))
        .def("positions", static_cast<void (Frame::*)(const Array3D&)>(&Frame::positions))
        .def("velocities", py::make_function(
            static_cast<const Array3D& (Frame::*)(void) const>(&Frame::velocities),
            py::return_value_policy<Array3D_convertor>()))
        .def("velocities", static_cast<void (Frame::*)(const Array3D&)>(&Frame::positions))
        .def("has_velocities", &Frame::has_velocities)
        .def("__len__", &Frame::natoms)
        .def("natoms", &Frame::natoms)
        .def("topology", py::make_function(
            static_cast<const Topology& (Frame::*)(void) const>(&Frame::topology),
            py::return_value_policy<py::copy_const_reference>()))
        .def("topology", static_cast<void (Frame::*)(const Topology&)>(&Frame::topology))
        .def("cell", py::make_function(
            static_cast<const UnitCell& (Frame::*)(void) const>(&Frame::cell),
            py::return_value_policy<py::copy_const_reference>()))
        .def("cell", static_cast<void (Frame::*)(const UnitCell&)>(&Frame::cell))
        .def("step", static_cast<size_t (Frame::*)(void) const>(&Frame::step))
        .def("step", static_cast<void (Frame::*)(size_t)>(&Frame::step))
        .def("guess_topology", &Frame::guess_topology)
    ;
}
