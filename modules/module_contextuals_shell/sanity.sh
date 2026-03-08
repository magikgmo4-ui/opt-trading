#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LIB_DIR="$SCRIPT_DIR/lib"
EXAMPLES_DIR="$SCRIPT_DIR/examples"

echo "Checking module_contextuals_shell..."

echo -n "Checking Structure... "
[ -d "$LIB_DIR" ] || { echo "FAIL: lib/ missing"; exit 1; }
[ -f "$LIB_DIR/reader.sh" ] || { echo "FAIL: reader.sh missing"; exit 1; }
[ -f "$LIB_DIR/renderer.sh" ] || { echo "FAIL: renderer.sh missing"; exit 1; }
[ -f "$LIB_DIR/router.sh" ] || { echo "FAIL: router.sh missing"; exit 1; }
[ -f "$EXAMPLES_DIR/example.ctx" ] || { echo "FAIL: example.ctx missing"; exit 1; }
echo "OK"

echo -n "Checking Status... "
CTX_COUNT="$(find "$EXAMPLES_DIR" -maxdepth 1 -type f -name '*.ctx' | wc -l | tr -d ' ')"
LIB_COUNT="$(find "$LIB_DIR" -maxdepth 1 -type f -name '*.sh' | wc -l | tr -d ' ')"
if [ "${CTX_COUNT:-0}" -ge 1 ] && [ "${LIB_COUNT:-0}" -ge 3 ]; then
  echo "OK"
else
  echo "FAIL: Status check failed (contexts=$CTX_COUNT libs=$LIB_COUNT)"
  exit 1
fi

echo -n "Checking List Actions... "
if bash "$SCRIPT_DIR/cmd.sh" list | tr -d '\r' | grep -q "Dire Bonjour"; then
  echo "OK"
else
  echo "FAIL: List Actions failed"
  exit 1
fi

echo -n "Checking Contextual Format... "
FIELDS="$(grep -vE '^\s*#' "$EXAMPLES_DIR/example.ctx" | head -n 1 | tr -d '\r' | awk -F'|' '{print NF}')"
if [ "${FIELDS:-0}" -ge 10 ]; then
  echo "OK ($FIELDS fields)"
else
  echo "FAIL: Format mismatch (found $FIELDS fields, expected >= 10)"
  exit 1
fi

echo "Sanity Check Passed."
