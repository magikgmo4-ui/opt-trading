#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")"
SRC_DIR="$SCRIPT_DIR/src"
PYTHON="python3"

if ! command -v "$PYTHON" >/dev/null 2>&1; then
    PYTHON="python"
fi

export PYTHONPATH="$SRC_DIR${PYTHONPATH:+:$PYTHONPATH}"

"$PYTHON" -m memory_bricks_v1.cli "$@"
