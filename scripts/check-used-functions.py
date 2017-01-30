#!/usr/bin/env python
"""
Check that all the functions defined in the chemfiles-sys crate are
effectivelly used in the chemfiles binding.
"""
import os

# Function not used by the Python API
IGNORED = ["chfl_trajectory_set_topology_file", "chfl_trajectory_open"]
ROOT = os.path.dirname(os.path.dirname(__file__))


def functions_list():
    functions = []
    with open(os.path.join(ROOT, "src", "chemfiles", "ffi.py")) as fd:
        for line in fd:
            line = line.strip()
            if line.startswith("# Function"):
                name = line.split('"')[1]
                if name not in IGNORED:
                    functions.append(name)
    return functions


def read_all_source():
    source = ""
    for (dirpath, _, pathes) in os.walk(os.path.join(ROOT, "src")):
        for path in pathes:
            if path != "ffi.py":
                with open(os.path.join(ROOT, dirpath, path)) as fd:
                    source += fd.read()
    return source


def check_functions(functions, source):
    for function in functions:
        if function not in source:
            print("Missing: " + function)


if __name__ == '__main__':
    functions = functions_list()
    source = read_all_source()
    check_functions(functions, source)
