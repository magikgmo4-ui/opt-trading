#!/usr/bin/env bash
set -euo pipefail

BASE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
APP="$BASE/app/trading_lab_v1.py"
CMD="${1:-help}"
ARG2="${2:-}"
ARG3="${3:-}"
ARG4="${4:-}"
ARG5="${5:-}"

case "$CMD" in
  sanity) "$BASE/scripts/sanity.sh" ;;
  status) python3 "$APP" status ;;
  show-profile) python3 "$APP" show-profile ;;
  show-schemas) python3 "$APP" show-schemas ;;
  show-market-source) python3 "$APP" show-market-source ;;
  show-sessions) python3 "$APP" show-sessions ;;
  show-batch-dates) python3 "$APP" show-batch-dates "$ARG2" "$ARG3" ;;
  sample-event) python3 "$APP" sample-event ;;
  sample-trade) python3 "$APP" sample-trade ;;
  materialize-samples) python3 "$APP" materialize-samples ;;
  journal-status) python3 "$APP" journal-status ;;
  run-once) python3 "$APP" run-once "$ARG2" ;;
  extract-features) python3 "$APP" extract-features "$ARG2" "$ARG3" "$ARG4" ;;
  analyze-market-input) python3 "$APP" analyze-market-input "$ARG2" "$ARG3" "$ARG4" ;;
  batch-run) python3 "$APP" batch-run "$ARG2" "$ARG3" "$ARG4" "$ARG5" ;;
  batch-report) python3 "$APP" batch-report "$ARG2" "$ARG3" "$ARG4" ;;
  show-last-batch-report) python3 "$APP" show-last-batch-report ;;
  *)
    echo "Usage: cmd.sh <command>"
    exit 1
    ;;
esac
