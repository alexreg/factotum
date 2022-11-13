#!/usr/bin/env bash -ex

mypy factotum factotum_cli
black factotum factotum_cli tests --check
isort factotum factotum_cli tests --check-only
