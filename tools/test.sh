#!/bin/bash -e

# Activate the environment
source ./tools/env.sh

# Execute all tests
pytest -rsxX --disable-warnings --cov=yeast --cov-report=term --cov-report=html:test/coverage ./tests/

echo ""
echo "Testing complete! Glad to be of service."
echo ""
