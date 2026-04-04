#!/usr/bin/env bash
set -euo pipefail

BASE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
# shellcheck source=/dev/null
source "$BASE/app/gateway_env.sh"

help_msg() {
  cat <<'EOF'
Usage:
  cmd.sh sanity
  cmd.sh status
  cmd.sh start
  cmd.sh stop
  cmd.sh logs
  cmd.sh attach
  cmd.sh health
  cmd.sh probe
  cmd.sh paths
EOF
}

case "${1:-help}" in
  sanity)
    "$BASE/scripts/sanity.sh"
    ;;
  status)
    require_target_user
    print_common
    if has_session; then
      echo "SESSION_STATUS=running"
    else
      echo "SESSION_STATUS=stopped"
    fi
    echo
    openclaw gateway health || true
    openclaw gateway probe || true
    ;;
  start)
    "$BASE/scripts/start.sh"
    ;;
  stop)
    "$BASE/scripts/stop.sh"
    ;;
  logs)
    "$BASE/scripts/logs.sh"
    ;;
  attach)
    "$BASE/scripts/attach.sh"
    ;;
  health)
    require_target_user
    openclaw gateway health
    ;;
  probe)
    require_target_user
    openclaw gateway probe
    ;;
  paths)
    require_target_user
    print_common
    ;;
  *)
    help_msg
    exit 1
    ;;
esac
