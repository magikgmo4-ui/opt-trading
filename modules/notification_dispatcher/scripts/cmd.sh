#!/usr/bin/env bash
set -euo pipefail
BASE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

help_msg() {
  cat <<'EOF'
Usage:
  cmd.sh sanity
  cmd.sh test
  cmd.sh send <event_type> [key=value ...]    — envoie via Telegram (TELEGRAM_BOT_TOKEN requis)
  cmd.sh dry  <event_type> [key=value ...]    — dry-run (pas de Telegram)

Event types:
  signal_received  proposition_generated  approval_required
  trade_executed   result_known  pipeline_error  pipeline_info
EOF
}

case "${1:-help}" in
  sanity)
    bash "$BASE/scripts/sanity.sh"
    ;;

  test)
    cd "$BASE"
    python3 -m unittest tests.test_dispatcher -v
    ;;

  send)
    shift
    event_type="${1:-pipeline_info}"
    shift || true
    cd "$BASE"
    python3 -m app "$event_type" "$@"
    ;;

  dry)
    shift
    event_type="${1:-pipeline_info}"
    shift || true
    cd "$BASE"
    python3 -m app "$event_type" --dry-run "$@"
    ;;

  help|--help|-h)
    help_msg
    ;;

  *)
    echo "unknown: ${1:-}" >&2; help_msg >&2; exit 1
    ;;
esac
