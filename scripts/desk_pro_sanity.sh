#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

# shellcheck disable=SC1091
source ./scripts/load_env.sh

echo "=== Desk Pro Sanity Check ==="
echo "Repo: $ROOT"
echo "Base URL: $TV_PERF_BASE_URL"
echo

req=(
  "modules/desk_pro/models.py"
  "modules/desk_pro/service/aggregator.py"
  "modules/desk_pro/service/scoring.py"
  "modules/desk_pro/api/routes.py"
  "scripts/load_env.sh"
)
missing=0
for f in "${req[@]}"; do
  if [[ ! -f "$f" ]]; then
    echo "MISSING: $f"
    missing=1
  else
    echo "OK file: $f"
  fi
done
if [[ "$missing" -eq 1 ]]; then
  echo "FAIL: missing files"
  exit 2
fi

python - <<'PY'
from modules.desk_pro.models import DeskForm, SRLevel
from modules.desk_pro.service.aggregator import build_snapshot_mock
from modules.desk_pro.service.scoring import compute_probability
from modules.desk_pro.api.routes import router

form = DeskForm(sr=[SRLevel(tf="W", kind="S", level=67900)])
snap = build_snapshot_mock()
res = compute_probability(form, snap)

print("OK import router prefix:", router.prefix)
print("OK snapshot metrics:", len(snap.metrics))
print("OK probability:", res.probability, "score:", res.score)
PY

echo "PASS: Desk Pro sanity OK"
