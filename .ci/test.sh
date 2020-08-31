#!/usr/bin/env bash

pre-commit run --all-files
pip install dist/*.whl
pytest -s -v
