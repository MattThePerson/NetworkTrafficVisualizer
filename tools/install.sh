#!/bin/bash

set -e

# check run as root
if [[ $EUID -eq 0 ]]; then
    echo "Please re-run install.sh without root (no sudo)"
    exit 1
fi

# check uv available
if command -v uv &>/dev/null; then
    echo "uv available"
    USE_UV=1
else
    echo "uv NOT available"
    USE_UV=0
fi

# .venv exists
if [[ -d ".venv" ]]; then
    echo ".venv exists"
    exit 0
fi

echo "Creating virtual environment..."
if [[ $USE_UV -eq 1 ]]; then
    uv venv .venv
else
    python3 -m venv .venv
fi

echo "Installing dependencies..."
if [[ $USE_UV -eq 1 ]]; then
    uv pip install -r requirements.txt
else
    .venv/bin/pip install -r requirements.txt
fi
