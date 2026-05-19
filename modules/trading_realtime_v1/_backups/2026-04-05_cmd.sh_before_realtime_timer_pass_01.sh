#!/usr/bin/env bash
set -euo pipefail
BASE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
APP="$BASE/app/trading_realtime_v1.py"
BRIDGE_APP="$BASE/app/event_bridge_v1.py"
REPORT_APP="$BASE/app/reporting_v1.py"
EXPORT_APP="$BASE/app/export_v1.py"
LOOP_APP="$BASE/app/runtime_loop_v1.py"
GUARD_APP="$BASE/app/guardrails_v1.py"
C="${1:-help}"
A2="${2:-}"
A3="${3:-}"
A4="${4:-}"
case "$C" in
  sanity) "$BASE/scripts/sanity.sh" ;;
  status) python3 "$APP" status ;;
  show-profile) python3 "$APP" show-profile ;;
  show-schemas) python3 "$APP" show-schemas ;;
  show-live-source) python3 "$APP" show-live-source ;;
  observe-once) python3 "$APP" observe-once "$A2" ;;
  runtime-status) python3 "$APP" runtime-status ;;
  bridge-status) python3 "$BRIDGE_APP" status ;;
  bridge-latest) python3 "$BRIDGE_APP" bridge-latest ;;
  show-last-runtime-event) python3 "$BRIDGE_APP" show-last-event ;;
  reporting-status) python3 "$REPORT_APP" status ;;
  report-runtime) python3 "$REPORT_APP" report-runtime "$A2" "$A3" "$A4" ;;
  show-last-runtime-report) python3 "$REPORT_APP" show-last-report ;;
  export-status) python3 "$EXPORT_APP" status ;;
  export-last-runtime-report) python3 "$EXPORT_APP" export-last ;;
  export-runtime-report) python3 "$EXPORT_APP" export-new "$A2" "$A3" "$A4" ;;
  runtime-loop-status) python3 "$LOOP_APP" status ;;
  runtime-loop-once) python3 "$LOOP_APP" run-once "$A2" ;;
  show-last-runtime-loop-run) python3 "$LOOP_APP" show-last-run ;;
  guardrails-status) python3 "$GUARD_APP" status ;;
  check-guardrails) python3 "$GUARD_APP" check-guardrails ;;
  show-last-guardrails-report) python3 "$GUARD_APP" show-last-report ;;
  *) echo "Usage: cmd.sh <command>"; exit 1 ;;
esac
