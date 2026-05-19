#!/usr/bin/env bash
set -euo pipefail

SCRIPT="${BASH_SOURCE[0]}"
if command -v readlink >/dev/null 2>&1; then
  SCRIPT="$(readlink -f "$SCRIPT" 2>/dev/null || echo "$SCRIPT")"
fi
BASE="$(cd "$(dirname "$SCRIPT")/.." && pwd)"
PY="$BASE/analyze_latest.py"

: "${INDEX_FILE:=/opt/trading/desk/snapshots/latest.json}"

echo "=== desk_analyze sanity ==="
date -Iseconds
echo

command -v python3 >/dev/null && python3 --version || { echo "ERROR: python3 missing"; exit 1; }
[[ -x "$PY" ]] || { echo "ERROR: missing $PY"; exit 1; }
[[ -f "$INDEX_FILE" ]] || { echo "ERROR: latest.json missing: $INDEX_FILE"; exit 1; }

python3 "$PY" --index "$INDEX_FILE" >/dev/null
echo "PASS: desk_analyze sanity OK"
