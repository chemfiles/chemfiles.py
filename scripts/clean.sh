#!/usr/bin/env bash

set -ex

find . -name "*.pyc" -delete
find . -name "__pycache__" | xargs rm -rf

rm -rf .tox
rm -rf _skbuild
rm -rf dist
rm -rf MANIFEST
rm -rf chemfiles.egg-info
rm -rf chemfiles/lib
rm -rf chemfiles/include
rm -rf chemfiles/external.py
