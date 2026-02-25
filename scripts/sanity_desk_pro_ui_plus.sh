#!/usr/bin/env bash
set -euo pipefail

REPO="${REPO:-/opt/trading}"
BASE_URL="${BASE_URL:-http://127.0.0.1:8010}"

echo "=== Desk Pro UI+Diagnostics+Logs Sanity Check ==="
echo "Repo: $REPO"
echo "Base URL: $BASE_URL"

TARGET="$REPO/modules/desk_pro/api/routes.py"

grep -n '"/logs/latest"' "$TARGET" >/dev/null || { echo "FAIL: /logs/latest route not found in routes.py"; exit 2; }
echo "OK: /logs/latest route found in routes.py"

if command -v curl >/dev/null 2>&1; then
  code="$(curl -s -o /dev/null -w "%{http_code}" "$BASE_URL/desk/logs/latest?n=5" || true)"
  [[ "$code" == "200" ]] || { echo "FAIL HTTP: /desk/logs/latest returned $code"; exit 3; }
  echo "OK HTTP: /desk/logs/latest 200"

  html="$(curl -sS "$BASE_URL/desk/ui" || true)"
  echo "$html" | grep -q "/desk/toolbox" && echo "OK: UI contains /desk/toolbox link" || echo "WARN: UI missing /desk/toolbox link (heuristic may not match)"
else
  echo "WARN curl not installed; skipping HTTP checks."
fi

echo "PASS: UI+Diagnostics+Logs sanity OK (or WARN for UI link)"
