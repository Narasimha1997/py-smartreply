#!/bin/bash

mkdir -p ${PWD}/dependencies

pushd ${PWD}/dependencies

    git clone https://github.com/google/re2.git

    git clone https://github.com/pybind/pybind11.git

    git clone https://github.com/tensorflow/tensorflow
    cd tensorflow && git checkout r2.4 && cd ..

popd