#!/usr/bin/env bash
set -euo pipefail

BASE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
APP="$BASE/app/trading_lab_v1.py"

case "${1:-help}" in
  sanity)
    "$BASE/scripts/sanity.sh"
    ;;
  status)
    python3 "$APP" status
    ;;
  show-profile)
    python3 "$APP" show-profile
    ;;
  show-schemas)
    python3 "$APP" show-schemas
    ;;
  show-market-source)
    python3 "$APP" show-market-source
    ;;
  show-sessions)
    python3 "$APP" show-sessions
    ;;
  sample-event)
    python3 "$APP" sample-event
    ;;
  sample-trade)
    python3 "$APP" sample-trade
    ;;
  materialize-samples)
    python3 "$APP" materialize-samples
    ;;
  journal-status)
    python3 "$APP" journal-status
    ;;
  run-once)
    python3 "$APP" run-once "${2:-}"
    ;;
  analyze-market-input)
    python3 "$APP" analyze-market-input "${2:-}" "${3:-}" "${4:-}"
    ;;
  *)
    echo "Usage: cmd.sh sanity|status|show-profile|show-schemas|show-market-source|show-sessions|sample-event|sample-trade|materialize-samples|journal-status|run-once [session_id]|analyze-market-input [csv_path] [session_id] [local_date]"
    exit 1
    ;;
esac
