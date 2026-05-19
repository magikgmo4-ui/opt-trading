#!/usr/bin/env bash
set -euo pipefail
BASE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
APP="$BASE/app/trading_realtime_v1.py"
BRIDGE_APP="$BASE/app/event_bridge_v1.py"
REPORT_APP="$BASE/app/reporting_v1.py"
EXPORT_APP="$BASE/app/export_v1.py"
LOOP_APP="$BASE/app/runtime_loop_v1.py"
GUARD_APP="$BASE/app/guardrails_v1.py"
TIMER_APP="$BASE/app/timer_v1.py"

[ -f "$APP" ] || exit 1
[ -f "$BRIDGE_APP" ] || exit 1
[ -f "$REPORT_APP" ] || exit 1
[ -f "$EXPORT_APP" ] || exit 1
[ -f "$LOOP_APP" ] || exit 1
[ -f "$GUARD_APP" ] || exit 1
[ -f "$TIMER_APP" ] || exit 1
command -v python3 >/dev/null 2>&1 || exit 1
echo "PASS: trading_realtime_v1 sanity OK"
