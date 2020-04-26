#!/bin/bash -e

# Repo root directory
REPO_ROOT_DIR="$(git rev-parse --show-toplevel)"

# Activate the environment
source ./tools/env.sh

# Lint the entire gushin_wrangler folder
flake8 --count --max-line-length=100 --ignore=E121,E123,E126,E226,E24,E704,W503,W504,W605 --statistics ${REPO_ROOT_DIR}/yeast

echo ""
echo "Lint complete! Glad to be of service."
echo ""
