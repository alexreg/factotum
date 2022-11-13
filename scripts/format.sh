#!/usr/bin/env bash -ex

autoflake --remove-all-unused-imports --recursive --remove-unused-variables --in-place factotum factotum_cli tests --exclude=__init__.py
black factotum factotum_cli tests
isort factotum factotum_cli tests
