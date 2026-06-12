#!/usr/bin/env bash
# TradingView Orchestrator — CLI entry point
set -euo pipefail

MOD="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REPO="$(cd "$MOD/../.." && pwd)"
RUNNER="$MOD/app/tv_runner.py"
PYTHON="${PYTHON:-python3}"

usage() {
  cat <<'EOF'
Usage:
  tv-orchestrator snapshot                     # Read-only: full TradingView state
  tv-orchestrator alert-list                   # Read-only: list all alerts
  tv-orchestrator screenshot                   # Read-only: capture chart screenshot
  tv-orchestrator run <packet.json>            # Read-only job from packet
  tv-orchestrator run <packet.json> --gate-approved   # Mutation job (write)
  tv-orchestrator run <packet.json> --dry-run  # Dry-run: show PS1 without executing
  tv-orchestrator new <type> [params_json]     # Generate a job packet template
  tv-orchestrator sanity                       # Run sanity check
  tv-orchestrator menu                         # Interactive menu
EOF
  exit 0
}

sanity() { bash "$MOD/scripts/sanity_check.sh"; }
menu_cmd() { bash "$MOD/scripts/menu.sh"; }

make_packet() {
  local jtype="$1"
  local params="${2:-{}}"
  local jid="tv_job_$(date +%Y%m%d)_$(echo "$jtype" | tr '.' '_')"
  local gate="pending"
  case "$jtype" in
    snapshot|alert.list|screenshot) gate="approved" ;;
    *) gate="pending" ;;
  esac
  python3 -c "
import json, sys
packet = {
  'schema': 'tv_job_v1',
  'id': '$jid',
  'type': '$jtype',
  'params': json.loads('$params'),
  'gate': '$gate',
  'created_at': __import__('datetime').datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'),
  'approved_at': None,
  'approved_by': None,
  'status': 'pending',
  'notes': ''
}
print(json.dumps(packet, indent=2))
"
}

run_quick_job() {
  local jtype="$1"
  local tmp
  tmp="$(mktemp /tmp/tv_job_XXXXXX.json)"
  make_packet "$jtype" > "$tmp"
  "$PYTHON" "$RUNNER" "$tmp"
  rm -f "$tmp"
}

[[ $# -eq 0 ]] && usage

CMD="$1"; shift

case "$CMD" in
  snapshot)    run_quick_job "snapshot" ;;
  alert-list)  run_quick_job "alert.list" ;;
  screenshot)  run_quick_job "screenshot" ;;
  run)
    [[ $# -lt 1 ]] && { echo "Usage: tv-orchestrator run <packet.json> [--gate-approved|--dry-run]"; exit 1; }
    "$PYTHON" "$RUNNER" "$@"
    ;;
  new)
    [[ $# -lt 1 ]] && { echo "Usage: tv-orchestrator new <type> [params_json]"; exit 1; }
    make_packet "$1" "${2:-{}}"
    ;;
  sanity) sanity ;;
  menu)   menu_cmd ;;
  help|-h|--help) usage ;;
  *) echo "Unknown command: $CMD"; usage ;;
esac
