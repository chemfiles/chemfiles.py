#!/usr/bin/env bash

set -ex

find . -name "*.pyc" -delete
find . -name "__pycache__" | xargs rm -rf
find . -name ".mypy_cache" | xargs rm -rf

rm -rf .tox
rm -rf build
rm -rf dist
rm -rf MANIFEST
rm -rf .coverage
rm -rf src/chemfiles.egg-info
rm -rf doc/_build

rm -rf chemfiles/*.dylib
rm -rf chemfiles/*.so
rm -rf chemfiles/*.dll
rm -rf chemfiles/external.py
