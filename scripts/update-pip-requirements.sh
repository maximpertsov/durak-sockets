#!/bin/bash
set -eux

git log -m -1 --name-only | grep poetry.lock || git log -m -1 --name-only | grep pyproject.toml || exit 0

checksum=$(md5sum < requirements.txt)
poetry export -f requirements.txt --without-hashes > requirements.txt
md5sum requirements.txt | grep $checksum || git commit --amend --no-edit requirements.txt
