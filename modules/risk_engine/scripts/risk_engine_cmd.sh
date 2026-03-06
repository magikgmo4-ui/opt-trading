#!/usr/bin/env bash
set -euo pipefail

CMD="${1:-help}"

usage() {
  echo "Usage: cmd-risk_engine <cmd> [args...]"
  echo
  echo "Commands:"
  echo "  sanity          Run sanity checks"
  echo "  calc <entry> <sl> <balance>   Calculate position size"
  echo "  status          Check module status"
  echo
}

case "$CMD" in
  sanity)
    python3 modules/risk_engine/app/risk_calculator.py sanity
    ;;

  calc)
    ENTRY="${2:-0}"
    SL="${3:-0}"
    BAL="${4:-0}"
    python3 modules/risk_engine/app/risk_calculator.py calc "$ENTRY" "$SL" "$BAL"
    ;;

  status)
    echo "Module: Risk Engine"
    if [ -f "modules/risk_engine/app/risk_calculator.py" ]; then
      echo "Status: Installed"
    else
      echo "Status: Missing"
    fi
    ;;

  help|--help|-h) usage ;;
  *) usage ;;
esac
