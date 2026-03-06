#!/usr/bin/env bash
set -euo pipefail

echo "=== Position Engine Sanity ==="
date

need() { command -v "$1" >/dev/null 2>&1 || { echo "MISSING: $1"; exit 1; }; }
need python3

echo "[module]"
if [ -f "modules/position_engine/position_manager.py" ]; then
  echo "OK: position_manager.py found"
else
  echo "FAIL: position_manager.py missing"
  exit 1
fi

echo "[models]"
if [ -f "modules/position_engine/models.py" ]; then
  echo "OK: models.py found"
else
  echo "FAIL: models.py missing"
  exit 1
fi

echo "[test]"
# Verify basic position creation
RES=$(python3 modules/position_engine/position_manager.py test)
if [[ "$RES" == *"BTCUSDT"* ]]; then
  echo "OK: position lifecycle test passed"
else
  echo "FAIL: position lifecycle test failed: $RES"
  exit 1
fi

echo "PASS: position engine sanity OK"
