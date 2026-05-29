#!/usr/bin/env bash
set -euo pipefail
MOD="${0%/*}/.."
MOD="$(cd "$MOD" && pwd -P)"

[ -d "$MOD/service" ] || { echo "FAIL: service missing"; exit 2; }
[ -f "$MOD/service/signal_context_reader.py" ] || { echo "FAIL: signal_context_reader missing"; exit 2; }
[ -x "$MOD/scripts/cmd.sh" ] || { echo "FAIL: cmd.sh not executable"; exit 2; }
[ -x "$MOD/scripts/menu.sh" ] || { echo "FAIL: menu.sh not executable"; exit 2; }
echo "PASS: telegram_screener sanity OK"
