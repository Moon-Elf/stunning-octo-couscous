#!/usr/bin/env bash
set -euo pipefail

# Run the generator
python3 src/main.py

# Start a tiny HTTP server in the output directory
cd docs
python3 -m http.server 8888
