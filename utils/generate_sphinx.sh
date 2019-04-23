#!/usr/bin/env bash

mkdir -p docs/
sphinx-apidoc -f -o docs/source timemap
cd docs || exit
make html

