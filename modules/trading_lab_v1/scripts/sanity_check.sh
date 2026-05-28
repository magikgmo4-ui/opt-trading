#!/usr/bin/env bash
set -euo pipefail
MODULE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ROOT_DIR="$(cd "$MODULE_DIR/../.." && pwd)"
APP_DIR="$MODULE_DIR/app"
echo "=== sanity: trading_lab_v1 ==="
[ -f "$MODULE_DIR/scripts/cmd.sh" ] || { echo "FAIL: cmd.sh missing"; exit 1; }
[ -f "$APP_DIR/trading_lab_v1.py" ] || { echo "FAIL: trading_lab_v1.py missing"; exit 1; }
[ -f "$APP_DIR/comparator_v1.py" ] || { echo "FAIL: comparator_v1.py missing"; exit 1; }
command -v python3 &>/dev/null || { echo "FAIL: python3 not found"; exit 1; }
cd "$ROOT_DIR"
python3 -c "import modules.trading_lab_v1.app.trading_lab_v1" 2>&1 || { echo "FAIL: import trading_lab_v1 failed"; exit 1; }
echo "OK: import trading_lab_v1"
echo "PASS: trading_lab_v1 sanity OK"
