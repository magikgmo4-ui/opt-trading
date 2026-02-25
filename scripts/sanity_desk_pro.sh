#!/usr/bin/env bash
set -euo pipefail

REPO="${REPO:-/opt/trading}"
BASE_URL="${BASE_URL:-http://127.0.0.1:8010}"
PY="${PY:-python}"

echo "=== Desk Pro Sanity Check ==="
echo "Repo: $REPO"
echo "Base URL: $BASE_URL"

cd "$REPO"

# Basic file presence checks
need_files=(
  "modules/desk_pro/models.py"
  "modules/desk_pro/service/aggregator.py"
  "modules/desk_pro/service/scoring.py"
  "modules/desk_pro/api/routes.py"
  "scripts/load_env.sh"
)

for f in "${need_files[@]}"; do
  if [[ -f "$f" ]]; then
    echo "OK file: $f"
  else
    echo "FAIL missing file: $f"
    exit 2
  fi
done

# Import check (fast fail)
$PY - <<'PY'
import importlib
import sys
mods = [
  "modules.desk_pro.api.routes",
  "modules.desk_pro.service.aggregator",
  "modules.desk_pro.service.scoring",
]
for m in mods:
  importlib.import_module(m)
print("OK imports:", ", ".join(mods))
PY

# If server is up, check endpoints (GET, not HEAD)
if command -v curl >/dev/null 2>&1; then
  code="$(curl -s -o /dev/null -w "%{http_code}" "$BASE_URL/desk/ui" || true)"
  if [[ "$code" == "200" ]]; then
    echo "OK HTTP: /desk/ui 200"
  else
    echo "WARN HTTP: /desk/ui returned $code (server might be down)."
  fi
else
  echo "WARN curl not installed; skipping HTTP check."
fi

echo "PASS: Desk Pro sanity OK"
echo '{"ok": true, "module": "desk_pro"}'
