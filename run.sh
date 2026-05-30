#!/bin/bash

# Check if running as root
if [[ $EUID -ne 0 ]]; then
    echo "This script must be run as root. Re-run with: sudo $0"
    exit 1
fi

cleanup() {
    deactivate
}
trap cleanup SIGINT

source .venv/bin/activate
.venv/bin/python3 main.py "$@"
