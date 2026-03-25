#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
MODULE_DIR=$(CDPATH= cd -- "$SCRIPT_DIR/.." && pwd)
REPO_ROOT=$(CDPATH= cd -- "$MODULE_DIR/../.." && pwd)

export PYTHONPATH="$REPO_ROOT/packages/collectors_core/src:$MODULE_DIR/src${PYTHONPATH:+:$PYTHONPATH}"

python3 - <<'PY'
import sys
if sys.version_info < (3, 11):
    raise SystemExit("Python 3.11 or newer is required")
PY

python3 -m collector_binance_spot.cli --module-dir "$MODULE_DIR" sanity
