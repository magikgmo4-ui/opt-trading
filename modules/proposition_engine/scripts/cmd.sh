#!/usr/bin/env bash
set -euo pipefail
BASE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

help_msg() {
  cat <<'EOF'
Usage:
  cmd.sh sanity
  cmd.sh test
  cmd.sh dry  <ticker> <side> <price> <tf> [--strategy-id X] [--sl N] [--tp N]
  cmd.sh propose <ticker> <side> <price> <tf> [--strategy-id X] [--timeout N]

Examples:
  cmd.sh dry BTCUSDT BUY 65000 1h
  cmd.sh dry ETHUSDT SELL 3000 4h --sl 3100 --tp 2800
  cmd.sh propose BTCUSDT BUY 65000 1h --timeout 90   # nécessite OpenClaw gateway
EOF
}

case "${1:-help}" in
  sanity)
    bash "$BASE/scripts/sanity.sh"
    ;;

  test)
    cd "$BASE"
    python3 -m unittest tests.test_proposition -v
    ;;

  dry)
    shift
    ticker="${1:-BTCUSDT}"; side="${2:-BUY}"; price="${3:-65000}"; tf="${4:-1h}"
    shift 4 || true
    cd "$BASE"
    python3 -m app "$ticker" "$side" "$price" "$tf" --dry-run "$@"
    ;;

  propose)
    shift
    ticker="${1:-BTCUSDT}"; side="${2:-BUY}"; price="${3:-65000}"; tf="${4:-1h}"
    shift 4 || true
    cd "$BASE"
    python3 -m app "$ticker" "$side" "$price" "$tf" "$@"
    ;;

  help|--help|-h)
    help_msg
    ;;

  *)
    echo "unknown: ${1:-}" >&2; help_msg >&2; exit 1
    ;;
esac
