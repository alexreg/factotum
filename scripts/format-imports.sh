#!/usr/bin/env bash -ex

# Sort imports one per line, so autoflake can remove unused imports
isort --recursive --force-single-line-imports --thirdparty factotum_cli --apply factotum factotum_cli tests

./scripts/format.sh
