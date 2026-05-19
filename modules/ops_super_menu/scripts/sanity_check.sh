#!/usr/bin/env bash
set -euo pipefail
SCRIPT_PATH="$(readlink -f "${BASH_SOURCE[0]}")"
SCRIPT_DIR="$(cd "$(dirname "$SCRIPT_PATH")" && pwd)"
BASE="$(cd "$SCRIPT_DIR/.." && pwd)"
echo "=== ops_super_menu sanity ==="
date -Iseconds
test -f "$BASE/ops_super_menu.sh" || { echo "FAIL: missing ops_super_menu.sh"; exit 1; }
bash -n "$BASE/ops_super_menu.sh"
echo "PASS: sanity OK"
