#!/usr/bin/env bash
set -euo pipefail
BASE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
[ -f "$BASE/app/trading_realtime_v1.py" ] || exit 1
[ -f "$BASE/app/event_bridge_v1.py" ] || exit 1
[ -f "$BASE/app/reporting_v1.py" ] || exit 1
[ -f "$BASE/app/export_v1.py" ] || exit 1
[ -f "$BASE/app/runtime_loop_v1.py" ] || exit 1
[ -f "$BASE/app/guardrails_v1.py" ] || exit 1
command -v python3 >/dev/null 2>&1 || exit 1
echo "PASS: trading_realtime_v1 sanity OK"
