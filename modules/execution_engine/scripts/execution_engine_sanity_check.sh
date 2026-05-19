#!/usr/bin/env bash
set -euo pipefail

echo "=== Execution Engine Sanity ==="
date

need() { command -v "$1" >/dev/null 2>&1 || { echo "MISSING: $1"; exit 1; }; }
need python3

echo "[module]"
if [ -f "modules/execution_engine/executor.py" ]; then
  echo "OK: executor.py found"
else
  echo "FAIL: executor.py missing"
  exit 1
fi

echo "[adapter]"
if [ -f "modules/execution_engine/adapters/paper.py" ]; then
  echo "OK: paper adapter found"
else
  echo "FAIL: paper adapter missing"
  exit 1
fi

echo "[test]"
# Verify basic execution flow
RES=$(python3 modules/execution_engine/executor.py test)
if [[ "$RES" == *"filled"* ]]; then
  echo "OK: execution test passed"
else
  echo "FAIL: execution test failed: $RES"
  exit 1
fi

echo "PASS: execution engine sanity OK"
