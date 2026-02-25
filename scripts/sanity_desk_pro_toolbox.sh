#!/usr/bin/env bash
set -euo pipefail

REPO="${REPO:-/opt/trading}"
BASE_URL="${BASE_URL:-http://127.0.0.1:8010}"

echo "=== Desk Pro Toolbox Sanity Check ==="
echo "Repo: $REPO"
echo "Base URL: $BASE_URL"

TARGET="$REPO/modules/desk_pro/api/routes.py"
grep -n '"/toolbox"' "$TARGET" >/dev/null || { echo "FAIL: toolbox route not found in $TARGET"; exit 2; }
echo "OK: toolbox route found in routes.py"

if command -v curl >/dev/null 2>&1; then
  code="$(curl -s -o /dev/null -w "%{http_code}" "$BASE_URL/desk/toolbox" || true)"
  if [[ "$code" == "200" ]]; then
    echo "OK HTTP: /desk/toolbox 200"
  else
    echo "FAIL HTTP: /desk/toolbox returned $code"
    exit 3
  fi
else
  echo "WARN curl not installed; skipping HTTP check."
fi

echo "PASS: Toolbox sanity OK"
