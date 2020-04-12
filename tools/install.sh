#!/bin/bash -e

# Repo root directory
REPO_ROOT_DIR="$(git rev-parse --show-toplevel)"

# Get the environment name
environment_header=$(head -n 1 environment.yml)
environment_name=${environment_header/name: /}
echo ""
echo "Generating environment: ${environment_name}"
echo ""

echo -n "  - Checking that conda is properly installed    "
conda -V >> /dev/null 2>&1 || { echo >&2 "Conda not found. Please download it from: http://conda.pydata.org/miniconda.html and run this script again"; exit 1; }
echo "[complete]"

echo -n "  - Exporting conda defaults                     "
eval "$(conda shell.bash hook)"
echo "[complete]"

echo -n "  - Removing the previous environment            "
conda remove --yes --quiet  -n ${environment_name} --all || { echo "Conda environment '${environment_name}' not found. Creating a new one."; }
echo "[complete]"

echo -n "  - Installing the environment                   "
conda env create --quiet --force -f environment.yml || { echo "There was a problem creating the environment"; }
echo "[complete]"

echo -n "  - Testing the environment                      "
conda activate ${environment_name}  || { echo "There was a problem activating the ${environment_name} environment"; }
echo "[complete]"

echo ""
echo "Installation complete! Glad to be of service."
echo ""
