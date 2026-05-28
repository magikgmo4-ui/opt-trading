#!/usr/bin/env bash
set -euo pipefail
MODULE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
NAME="$(basename "$MODULE_DIR")"
echo "=== sanity: $NAME ==="
[ -f "$MODULE_DIR/scripts/cmd.sh" ] || { echo "FAIL: cmd.sh missing"; exit 1; }
[ -f "$MODULE_DIR/scripts/menu.sh" ] || { echo "FAIL: menu.sh missing"; exit 1; }
[ -f "$MODULE_DIR/README.md" ] || echo "WARN: README.md missing"
echo "PASS: $NAME sanity OK"
