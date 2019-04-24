#!/usr/bin/env bash

pip install dist/*.whl
pytest -s -v

