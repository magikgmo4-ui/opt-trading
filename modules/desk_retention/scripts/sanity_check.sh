#!/usr/bin/env bash
set -euo pipefail
BASE="$(cd "$(dirname "$0")/.." && pwd)"
echo "=== desk_retention sanity ==="
date -Iseconds

command -v find >/dev/null 2>&1 || { echo "FAIL: find missing"; exit 1; }

CFG="$BASE/config/desk_retention.env"
if [ ! -f "$CFG" ]; then
  echo "WARN: config missing: $CFG"
  echo "Tip: cp $BASE/config/desk_retention.env.example $CFG"
else
  echo "OK: config found: $CFG"
fi

echo "PASS: sanity OK"
