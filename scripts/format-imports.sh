#!/usr/bin/env bash -ex

# Sort imports one per line, so autoflake can remove unused imports
isort --recursive --force-single-line-imports --thirdparty factotum --apply factotum tests

./scripts/format.sh
