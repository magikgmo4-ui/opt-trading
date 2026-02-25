#!/usr/bin/env bash
set -euo pipefail
REPO="${REPO:-/opt/trading}"
BASE_URL="${BASE_URL:-http://127.0.0.1:8010}"

echo "=== Sanity: Desk Pro UI Toolbox Fix ==="
echo "Repo: $REPO"
echo "Base URL: $BASE_URL"

python - <<'PY'
from modules.desk_pro.api.routes import ui
resp = ui()
body = getattr(resp, "body", b"").decode("utf-8","ignore")
print("HAS /desk/form:", "/desk/form" in body)
print("HAS /desk/toolbox:", "/desk/toolbox" in body)
if "/desk/toolbox" not in body:
    raise SystemExit(2)
PY

if command -v curl >/dev/null 2>&1; then
  code="$(curl -s -o /dev/null -w "%{http_code}" "$BASE_URL/desk/ui" || true)"
  [[ "$code" == "200" ]] || { echo "FAIL HTTP: /desk/ui $code"; exit 3; }
  curl -sS "$BASE_URL/desk/ui" | grep -q "/desk/toolbox" && echo "OK HTTP: toolbox link present in /desk/ui" || { echo "FAIL HTTP: toolbox link absent in /desk/ui"; exit 4; }
else
  echo "WARN: curl not installed; skipping HTTP check."
fi

echo "PASS"
