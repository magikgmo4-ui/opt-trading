#!/usr/bin/env bash
set -euo pipefail
MODULE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ROOT_DIR="$(cd "$MODULE_DIR/../.." && pwd)"
APP_DIR="$MODULE_DIR/app"
echo "=== sanity: trading_realtime_v1 ==="
[ -f "$MODULE_DIR/scripts/cmd.sh" ] || { echo "FAIL: cmd.sh missing"; exit 1; }
[ -f "$APP_DIR/trading_realtime_v1.py" ] || { echo "FAIL: trading_realtime_v1.py missing"; exit 1; }
[ -f "$APP_DIR/guardrails_v1.py" ] || { echo "FAIL: guardrails_v1.py missing"; exit 1; }
[ -f "$APP_DIR/runtime_loop_v1.py" ] || { echo "FAIL: runtime_loop_v1.py missing"; exit 1; }
command -v python3 &>/dev/null || { echo "FAIL: python3 not found"; exit 1; }
cd "$ROOT_DIR"
python3 -c "import modules.trading_realtime_v1.app.guardrails_v1" 2>&1 || { echo "FAIL: import guardrails_v1 failed"; exit 1; }
echo "OK: import guardrails_v1"
echo "PASS: trading_realtime_v1 sanity OK"
