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
  sample-event)
    python3 "$APP" sample-event
    ;;
  sample-trade)
    python3 "$APP" sample-trade
    ;;
  materialize-samples)
    python3 "$APP" materialize-samples
    ;;
  *)
    echo "Usage: cmd.sh sanity|status|show-profile|show-schemas|sample-event|sample-trade|materialize-samples"
    exit 1
    ;;
esac
