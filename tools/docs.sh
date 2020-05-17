#!/bin/bash -e

# Repo root directory
REPO_ROOT_DIR="$(git rev-parse --show-toplevel)"

# Activate the environment
source ./tools/env.sh

# Notebooks to Markdown
jupyter nbconvert --to markdown docs/examples/students.ipynb
jupyter nbconvert --to markdown docs/examples/working_with_strings.ipynb

# Build and Serve docs
PYTHONPATH=${REPO_ROOT_DIR}/yeast:$PYTHONPATH
cd ${REPO_ROOT_DIR}
mkdocs build
mkdocs serve

# To deploy the documentation:
# mkdocs gh-deploy
