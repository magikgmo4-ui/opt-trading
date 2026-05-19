#!/usr/bin/env bash
set -euo pipefail

SCRIPT="${BASH_SOURCE[0]}"
if command -v readlink >/dev/null 2>&1; then
  SCRIPT="$(readlink -f "$SCRIPT" 2>/dev/null || echo "$SCRIPT")"
fi
MOD="$(cd "$(dirname "$SCRIPT")/.." && pwd -P)"
NAME="$(basename "$MOD")"

if [[ "$(basename "$0")" == "sanity-shared_sshfs_permanent" && -x "/opt/trading/scripts/shared_sshfs_permanent_sanity.sh" ]]; then
  exec bash "/opt/trading/scripts/shared_sshfs_permanent_sanity.sh"
fi

echo "=== sanity (wrapper) ==="
echo "name=$NAME"
echo "path=$MOD"
[ -d "$MOD" ] || { echo "FAIL: module missing"; exit 2; }
[ -d "$MOD/scripts" ] || { echo "FAIL: scripts missing"; exit 2; }
[ -x "$MOD/scripts/menu.sh" ] || { echo "FAIL: menu.sh not executable"; exit 2; }
[ -x "$MOD/scripts/cmd.sh" ] || { echo "FAIL: cmd.sh not executable"; exit 2; }
echo "PASS: wrapper sanity OK"
