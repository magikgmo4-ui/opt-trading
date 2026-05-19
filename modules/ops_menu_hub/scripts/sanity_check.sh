#!/usr/bin/env bash
set -euo pipefail

SCRIPT_PATH="$(readlink -f "${BASH_SOURCE[0]}")"
SCRIPT_DIR="$(cd "$(dirname "$SCRIPT_PATH")" && pwd)"
BASE="$(cd "$SCRIPT_DIR/.." && pwd)"

echo "=== ops_menu_hub sanity ==="
date -Iseconds
test -d /opt/trading/modules || { echo "FAIL: /opt/trading/modules missing"; exit 1; }
test -f "$BASE/ops_menu_hub.sh" || { echo "FAIL: ops_menu_hub.sh missing"; exit 1; }
echo "PASS: sanity OK"
