#!/bin/bash -e

# Repo root directory
REPO_ROOT_DIR="$(git rev-parse --show-toplevel)"

# Activate the environment
source ./tools/env.sh

# Build and Serve docs
PYTHONPATH=${REPO_ROOT_DIR}/yeast:$PYTHONPATH
cd ${REPO_ROOT_DIR}
mkdocs build
mkdocs serve
