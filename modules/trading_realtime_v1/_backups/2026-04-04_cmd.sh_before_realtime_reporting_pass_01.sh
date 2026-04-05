#!/usr/bin/env bash
set -euo pipefail
BASE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
APP="$BASE/app/trading_realtime_v1.py"
BRIDGE_APP="$BASE/app/event_bridge_v1.py"

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
  show-live-source)
    python3 "$APP" show-live-source
    ;;
  observe-once)
    python3 "$APP" observe-once "${2:-}"
    ;;
  runtime-status)
    python3 "$APP" runtime-status
    ;;
  bridge-status)
    python3 "$BRIDGE_APP" status
    ;;
  bridge-latest)
    python3 "$BRIDGE_APP" bridge-latest
    ;;
  show-last-runtime-event)
    python3 "$BRIDGE_APP" show-last-event
    ;;
  *)
    echo "Usage: cmd.sh sanity|status|show-profile|show-schemas|show-live-source|observe-once [live_jsonl_path]|runtime-status|bridge-status|bridge-latest|show-last-runtime-event"
    exit 1
    ;;
esac
