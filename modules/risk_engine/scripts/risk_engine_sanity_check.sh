#!/usr/bin/env bash
set -euo pipefail

echo "=== Risk Engine Sanity ==="
date

need() { command -v "$1" >/dev/null 2>&1 || { echo "MISSING: $1"; exit 1; }; }

need python3

echo "[module]"
if [ -f "modules/risk_engine/app/risk_calculator.py" ]; then
  echo "OK: risk_calculator.py found"
else
  echo "FAIL: risk_calculator.py missing"
  exit 1
fi

echo "[test]"
python3 modules/risk_engine/app/risk_calculator.py sanity || { echo "FAIL: python execution failed"; exit 1; }

echo "PASS: risk_engine sanity OK"
