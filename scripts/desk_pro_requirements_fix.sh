#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

req="requirements.txt"
[[ -f "$req" ]] || { echo "FAIL: requirements.txt not found"; exit 2; }

if grep -qiE '^pydantic' "$req"; then
  echo "OK: pydantic already present in requirements.txt"
else
  echo 'pydantic<3' >> "$req"
  echo "OK: appended 'pydantic<3' to requirements.txt"
fi

echo "Installing into venv..."
./venv/bin/pip install -U pip >/dev/null
./venv/bin/pip install -r requirements.txt
echo "PASS: requirements installed"
