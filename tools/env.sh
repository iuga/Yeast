#!/bin/bash -e

# Make funcitons exported by default to be made available in subshells
eval "$(conda shell.bash hook)"

# Get the environment name
environment_header=$(head -n 1 environment.yml)
environment_name=${environment_header/name: /}

# Activate the environment
conda activate ${environment_name} || { echo "There was a problem activating the ${environment_name} environment"; }
