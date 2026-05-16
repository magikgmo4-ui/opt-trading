#!/usr/bin/env bash
set -euo pipefail

BASE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
GATEWAY_HEALTH_URL="http://127.0.0.1:18789/health"

help_msg() {
  cat <<'EOF'
Usage:
  cmd.sh sanity
  cmd.sh health
  cmd.sh test
  cmd.sh ask    "<instruction>" [--context "<ctx>"] [--timeout 60]
  cmd.sh build  "<instruction>" [--context "<ctx>"] [--timeout 60]
  cmd.sh evaluate "<instruction>" [--context "<ctx>"] [--timeout 60]
  cmd.sh review "<instruction>" [--context "<ctx>"] [--timeout 60]
EOF
}

case "${1:-help}" in
  sanity)
    bash "$BASE/scripts/sanity.sh"
    ;;

  health)
    echo "MODULE=openclaw_operator_bridge"
    gw=$(curl -sf --max-time 5 "$GATEWAY_HEALTH_URL" 2>/dev/null) && echo "GATEWAY=$gw" || echo "GATEWAY=unreachable"
    command -v openclaw >/dev/null 2>&1 && echo "OPENCLAW_CLI=found" || echo "OPENCLAW_CLI=missing"
    echo "STATUS=live"
    ;;

  test)
    cd "$BASE"
    python3 -m unittest tests.test_bridge_mock -v
    ;;

  ask|build|evaluate|review)
    action="$1"
    instruction="${2:-}"
    [ -n "$instruction" ] || { echo "FAIL: instruction required" >&2; exit 1; }
    shift 2 || shift 1
    cd "$BASE"
    python3 -m app "$action" "$instruction" "$@"
    ;;

  help|--help|-h)
    help_msg
    ;;

  *)
    echo "unknown command: ${1:-}" >&2
    help_msg >&2
    exit 1
    ;;
esac
