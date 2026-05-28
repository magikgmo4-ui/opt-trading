#!/usr/bin/env bash
set -euo pipefail
MODULE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ROOT_DIR="$(cd "$MODULE_DIR/../.." && pwd)"
APP_DIR="$MODULE_DIR/app"
NAME="$(basename "$MODULE_DIR")"
echo "=== sanity: $NAME ==="
[ -f "$MODULE_DIR/scripts/cmd.sh" ] || { echo "FAIL: cmd.sh missing"; exit 1; }
[ -d "$APP_DIR" ] || { echo "FAIL: app/ missing"; exit 1; }
[ -f "$APP_DIR/__main__.py" ] || { echo "FAIL: __main__.py missing"; exit 1; }
command -v python3 &>/dev/null || { echo "FAIL: python3 not found"; exit 1; }
cd "$ROOT_DIR"
python3 -c "import modules.datasheet_writer.app" 2>&1 || { echo "FAIL: import modules.datasheet_writer.app failed"; exit 1; }
echo "OK: import modules.datasheet_writer.app"
echo "PASS: $NAME sanity OK"
