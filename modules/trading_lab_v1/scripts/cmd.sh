#!/usr/bin/env bash
set -euo pipefail
BASE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
APP="$BASE/app/trading_lab_v1.py"
EXPORT_APP="$BASE/app/report_export_v1.py"
COMPARATOR_APP="$BASE/app/comparator_v1.py"
LIVE_APP="$BASE/app/live_observation_v1.py"
LIVE_EXPORT_APP="$BASE/app/live_export_v1.py"
CMD="${1:-help}"
A2="${2:-}"
A3="${3:-}"
A4="${4:-}"
A5="${5:-}"
case "$CMD" in
  sanity) "$BASE/scripts/sanity.sh" ;;
  status) python3 "$APP" status ;;
  show-profile) python3 "$APP" show-profile ;;
  show-schemas) python3 "$APP" show-schemas ;;
  show-market-source) python3 "$APP" show-market-source ;;
  show-sessions) python3 "$APP" show-sessions ;;
  show-batch-dates) python3 "$APP" show-batch-dates "$A2" "$A3" ;;
  sample-event) python3 "$APP" sample-event ;;
  sample-trade) python3 "$APP" sample-trade ;;
  materialize-samples) python3 "$APP" materialize-samples ;;
  journal-status) python3 "$APP" journal-status ;;
  run-once) python3 "$APP" run-once "$A2" ;;
  extract-features) python3 "$APP" extract-features "$A2" "$A3" "$A4" ;;
  analyze-market-input) python3 "$APP" analyze-market-input "$A2" "$A3" "$A4" ;;
  batch-run) python3 "$APP" batch-run "$A2" "$A3" "$A4" "$A5" ;;
  batch-report) python3 "$APP" batch-report "$A2" "$A3" "$A4" ;;
  show-last-batch-report) python3 "$APP" show-last-batch-report ;;
  export-last-batch-report) python3 "$EXPORT_APP" export-last ;;
  export-batch-report) python3 "$EXPORT_APP" export-new "$A2" "$A3" "$A4" ;;
  export-status) python3 "$EXPORT_APP" status ;;
  comparator-status) python3 "$COMPARATOR_APP" status ;;
  show-live-reference) python3 "$COMPARATOR_APP" show-live-source ;;
  compare-live) python3 "$COMPARATOR_APP" compare-live "$A2" "$A3" "$A4" "$A5" ;;
  show-last-comparator-report) python3 "$COMPARATOR_APP" show-last-report ;;
  live-observation-status) python3 "$LIVE_APP" status ;;
  show-live-observation-source) python3 "$LIVE_APP" show-source ;;
  observe-live) python3 "$LIVE_APP" observe-live "$A2" "$A3" "$A4" "$A5" ;;
  show-last-live-observation-run) python3 "$LIVE_APP" show-last-run ;;
  live-export-status) python3 "$LIVE_EXPORT_APP" status ;;
  export-last-live-observation) python3 "$LIVE_EXPORT_APP" export-last ;;
  export-live-observation) python3 "$LIVE_EXPORT_APP" export-new "$A2" "$A3" "$A4" "$A5" ;;
  param-sweep-run) python3 "$APP" param-sweep-run "$A2" "$A3" ;;
  param-sweep-batch) python3 "$APP" param-sweep-batch "$A2" ;;
  param-sweep-report) python3 "$APP" param-sweep-report ;;
  param-sweep-export) python3 "$APP" param-sweep-export ;;
  *) echo "Usage: cmd.sh <command>"; exit 1 ;; 
esac
