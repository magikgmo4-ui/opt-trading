#!/usr/bin/env bash
set -euo pipefail

SCRIPT_PATH="$(readlink -f "${BASH_SOURCE[0]}")"
SCRIPT_DIR="$(cd "$(dirname "$SCRIPT_PATH")" && pwd)"
BASE="$(cd "$SCRIPT_DIR/.." && pwd)"

echo "=== desk_state sanity ==="
date -Iseconds
python3 -V
test -f "$BASE/desk_state.py" || { echo "FAIL: desk_state.py missing"; exit 1; }
python3 -m py_compile "$BASE/desk_state.py" || { echo "FAIL: py_compile"; exit 1; }
echo "PASS: sanity OK"
