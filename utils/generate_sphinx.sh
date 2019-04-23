#!/usr/bin/env bash

sphinx-apidoc -f -o docs/source location_history
cd docs;
rm -rf wm-bcli || true
make html

