#!/bin/bash

# check run as root
if [[ $EUID -ne 0 ]]; then
    echo "This script must be run as root. Re-run with: sudo $0"
    exit 1
fi

# check .venv
if [[ ! -d ".venv" ]]; then
    echo ".venv not created, please run `tools/install.sh`"
fi

.venv/bin/python3 main.py "$@"
