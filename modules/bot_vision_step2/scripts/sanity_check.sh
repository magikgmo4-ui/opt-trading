#!/usr/bin/env bash
set -euo pipefail
MOD="${0%/*}/.."
MOD="$(cd "$MOD" && pwd -P)"
NAME="$(basename "$MOD")"
echo "=== sanity (wrapper) ==="
echo "name=$NAME"
echo "path=$MOD"
[ -d "$MOD" ] || { echo "FAIL: module missing"; exit 2; }
[ -d "$MOD/scripts" ] || { echo "FAIL: scripts missing"; exit 2; }
[ -x "$MOD/scripts/menu.sh" ] || { echo "FAIL: menu.sh not executable"; exit 2; }
[ -x "$MOD/scripts/cmd.sh" ] || { echo "FAIL: cmd.sh not executable"; exit 2; }
echo "PASS: wrapper sanity OK"
