#!/usr/bin/env bash
set -euo pipefail
MODULE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ROOT_DIR="$(cd "$MODULE_DIR/../.." && pwd)"
APP_DIR="$MODULE_DIR/app"
echo "=== sanity: validation_gate ==="
[ -f "$MODULE_DIR/scripts/cmd.sh" ] || { echo "FAIL: cmd.sh missing"; exit 1; }
[ -f "$APP_DIR/__main__.py" ] || { echo "FAIL: __main__.py missing"; exit 1; }
command -v python3 &>/dev/null || { echo "FAIL: python3 not found"; exit 1; }
cd "$ROOT_DIR"
python3 -c "import modules.validation_gate.app" 2>&1 || { echo "FAIL: import validation_gate failed"; exit 1; }
echo "OK: import validation_gate"
echo "PASS: validation_gate sanity OK"
