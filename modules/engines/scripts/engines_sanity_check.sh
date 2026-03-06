#!/usr/bin/env bash
set -euo pipefail

echo "=== Engines Plugin Sanity ==="
date

need() { command -v "$1" >/dev/null 2>&1 || { echo "MISSING: $1"; exit 1; }; }
need python3

echo "[registry]"
# Check that we can import the registry
python3 -c "import modules.engines.registry" || { echo "FAIL: registry import"; exit 1; }
echo "OK: registry importable"

echo "[router]"
# Check router basic function
python3 -c "import modules.engines.router" || { echo "FAIL: router import"; exit 1; }
echo "OK: router importable"

echo "[dummy]"
# Verify the built-in echo engine
RES=$(python3 -c "from modules.engines.registry import get_engine; print(get_engine('ECHO_TEST') is not None)")
if [ "$RES" == "True" ]; then
  echo "OK: ECHO_TEST registered"
else
  echo "FAIL: ECHO_TEST missing"
  exit 1
fi

echo "PASS: engines sanity OK"
