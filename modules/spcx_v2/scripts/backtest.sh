#!/usr/bin/env bash
set -euo pipefail
# SPCX V2 Backtest Scheduler
# GO_SPACEX_DAY1_ORDERFLOW_AND_OWNERSHIP_LEDGER_01
#
# Backtest schedule:
#   Intraday (live paper): runner --watch (poll events.jsonl every 5s)
#   End-of-day batch: runner --pipeline (enriched snapshot + orderflow/ownership)
#   EOD systemd timer: Mon-Fri 16:15 ET = 20:15 UTC

REPO_ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"
cd "$REPO_ROOT"

VENV_PYTHON="${REPO_ROOT}/venv/bin/python3"
PYTHON="${VENV_PYTHON:-python3}"

MODE="${1:-pipeline}"

case "$MODE" in
    pipeline|eod)
        echo "[$(date -Iseconds)] SPCX V2 EOD backtest (pipeline mode)..."
        "$PYTHON" -c "
from modules.spcx_v2.runner import run_pipeline_backtest
run_pipeline_backtest()
"
        ;;
    watch|live)
        echo "[$(date -Iseconds)] SPCX V2 live paper (watch mode)..."
        exec "$PYTHON" -m modules.spcx_v2.runner --watch
        ;;
    replay)
        FILE="${2:-state/events.jsonl}"
        echo "[$(date -Iseconds)] SPCX V2 replay $FILE ..."
        exec "$PYTHON" -m modules.spcx_v2.runner --replay "$FILE"
        ;;
    once)
        echo "[$(date -Iseconds)] SPCX V2 once..."
        exec "$PYTHON" -m modules.spcx_v2.runner --once
        ;;
    summary)
        echo "[$(date -Iseconds)] SPCX V2 summary..."
        exec "$PYTHON" -m modules.spcx_v2.runner --summary
        ;;
    *)
        echo "Usage: $0 {pipeline|eod|watch|live|replay FILE|once|summary}"
        exit 1
        ;;
esac

echo "[$(date -Iseconds)] Done."
