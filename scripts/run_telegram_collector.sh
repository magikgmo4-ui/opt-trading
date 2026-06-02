#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
REPO_ROOT=$(CDPATH= cd -- "$SCRIPT_DIR/.." && pwd)
MODULE_DIR="$REPO_ROOT/modules/collector_telegram"
PYTHON_BIN="python3"

if [ -x "$REPO_ROOT/venv/bin/python" ]; then
  PYTHON_BIN="$REPO_ROOT/venv/bin/python"
fi

export PYTHONPATH="$REPO_ROOT:$MODULE_DIR/src${PYTHONPATH:+:$PYTHONPATH}"

exec "$PYTHON_BIN" -m collector_telegram.cli --module-dir "$MODULE_DIR" "$@"
