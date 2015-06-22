#!/usr/bin/env bash

mkdir conda-build
cd conda-build
export MACOSX_DEPLOYMENT_TARGET=""
cmake -DBUILD_FRONTEND=OFF -DPYTHON_BINDING=ON -DCMAKE_INSTALL_PREFIX=$PREFIX ..
cmake --build . --target install --config release
