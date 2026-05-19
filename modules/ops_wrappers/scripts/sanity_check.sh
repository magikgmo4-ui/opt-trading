#!/usr/bin/env bash
set -euo pipefail
echo "=== ops_wrappers sanity ==="
date --iso-8601=seconds || true
ROOT="/opt/trading"
[ -d "$ROOT/modules" ] || { echo "FAIL: missing /opt/trading/modules"; exit 2; }
[ -x "$ROOT/modules/ops_wrappers/ops_wrappers.sh" ] || { echo "FAIL: missing ops_wrappers.sh"; exit 2; }
echo "PASS: sanity OK"
