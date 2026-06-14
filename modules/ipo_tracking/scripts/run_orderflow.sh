#!/usr/bin/env bash
set -euo pipefail
# SPCX Orderflow + Ownership Pipeline Runner
# GO_SPACEX_DAY1_ORDERFLOW_AND_OWNERSHIP_LEDGER_01
#
# Usage:
#   ./run_orderflow.sh              # live run
#   ./run_orderflow.sh --offline    # offline dry-run
#
# Can be called from cron or systemd timer.
# Recommended cron (market hours 9:30-16:00 ET = 13:30-20:00 UTC):
#   */1 13-19 * * 1-5  cd /opt/trading && ./modules/ipo_tracking/scripts/run_orderflow.sh

REPO_ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"
cd "$REPO_ROOT"

VENV_PYTHON="${REPO_ROOT}/venv/bin/python3"
if [ -f "$VENV_PYTHON" ]; then
    PYTHON="$VENV_PYTHON"
else
    PYTHON="python3"
fi

MODE="${1:-live}"

if [ "$MODE" = "--offline" ]; then
    echo "[$(date -Iseconds)] Running SPCX orderflow pipeline (offline)..."
    "$PYTHON" -c "
from modules.ipo_tracking.pipeline import run_full_pipeline
result = run_full_pipeline(offline=True)
print(f'ok={result[\"ok\"]} events={result.get(\"raw_events_count\",0)}')
"
else
    echo "[$(date -Iseconds)] Running SPCX orderflow pipeline (live)..."
    "$PYTHON" -c "
from modules.ipo_tracking.pipeline import run_full_pipeline
result = run_full_pipeline(offline=False)
import json
print(json.dumps({
    'ok': result.get('ok'),
    'events': result.get('raw_events_count', 0),
    'orderflow_score': result.get('orderflow_score', {}).get('score'),
    'ownership_score': result.get('ownership_score', {}).get('score'),
    'buckets': result.get('orderflow_bucket_count', 0),
}, default=str))
"
fi
echo "[$(date -Iseconds)] Done."
