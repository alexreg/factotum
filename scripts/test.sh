#!/usr/bin/env bash -ex

# Use `pytest --forked` to ensure modified `sys.path` for importing relative modules in examples
pytest --cov=factotum --cov=factotum_cli --cov=tests --cov-report=term-missing --cov-report=xml -o console_output_style=progress --forked --numprocesses=auto "$@"
