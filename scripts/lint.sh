#!/usr/bin/env bash -ex

mypy factotum
yapf --recursive --quiet factotum tests
# isort --check-only factotum tests
