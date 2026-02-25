#!/usr/bin/env bash
set -euo pipefail

BASE_URL="${BASE_URL:-http://127.0.0.1:8010}"
echo "=== Desk Pro UI Inject Sanity ==="
if command -v curl >/dev/null 2>&1; then
  code="$(curl -s -o /dev/null -w "%{http_code}" "$BASE_URL/desk/ui" || true)"
  [[ "$code" == "200" ]] || { echo "FAIL HTTP: /desk/ui $code"; exit 2; }
  html="$(curl -sS "$BASE_URL/desk/ui" || true)"
  echo "$html" | grep -q "/desk/toolbox" && echo "OK: /desk/toolbox link present" || { echo "FAIL: /desk/toolbox link missing"; exit 3; }
  echo "$html" | grep -q "Desk Pro — Diagnostics" && echo "OK: Diagnostics section present" || { echo "FAIL: Diagnostics section missing"; exit 4; }
  echo "PASS"
else
  echo "curl not found"
  exit 5
fi
