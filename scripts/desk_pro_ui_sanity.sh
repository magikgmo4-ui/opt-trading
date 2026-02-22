#!/usr/bin/env bash
set -euo pipefail
cd /opt/trading
# shellcheck disable=SC1091
source ./scripts/load_env.sh
URL="${TV_PERF_BASE_URL}/desk/ui"

echo "=== Desk Pro UI Sanity ==="
echo "URL: $URL"

code="$(curl -s -o /tmp/desk_ui.html -w '%{http_code}' "$URL")"
echo "HTTP: $code"
head -n 5 /tmp/desk_ui.html || true

[[ "$code" == "200" ]] || { echo "FAIL: UI not 200"; exit 2; }
grep -q "Desk Pro" /tmp/desk_ui.html && echo "PASS: UI contains title" || { echo "FAIL: UI missing title"; exit 2; }
