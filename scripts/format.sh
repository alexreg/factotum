#!/usr/bin/env bash -ex

autoflake --remove-all-unused-imports --recursive --remove-unused-variables --in-place factotum tests --exclude=__init__.py
yapf --in-place --recursive factotum tests
# isort factotum tests
