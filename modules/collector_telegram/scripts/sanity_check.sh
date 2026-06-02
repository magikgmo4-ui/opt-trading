#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
MODULE_DIR=$(CDPATH= cd -- "$SCRIPT_DIR/.." && pwd)
REPO_ROOT=$(CDPATH= cd -- "$MODULE_DIR/../.." && pwd)
PYTHON_BIN="python3"

if [ -x "$REPO_ROOT/venv/bin/python" ]; then
  PYTHON_BIN="$REPO_ROOT/venv/bin/python"
fi

export PYTHONPATH="$REPO_ROOT:$MODULE_DIR/src${PYTHONPATH:+:$PYTHONPATH}"

"$PYTHON_BIN" - <<'PY'
import sys
if sys.version_info < (3, 11):
    raise SystemExit("Python 3.11 or newer is required")
PY

"$PYTHON_BIN" -m collector_telegram.cli --module-dir "$MODULE_DIR" sanity
