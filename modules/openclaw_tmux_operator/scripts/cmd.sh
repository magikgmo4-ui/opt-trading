#!/usr/bin/env bash
set -Eeuo pipefail

cmd="${1:-}"
target="${2:-}"
session="${3:-}"

ROOT="/opt/trading"

case "$cmd" in
  fleet-status)
    cd "$ROOT"
    python3 modules/runtime_health/fleet_orchestrator.py --dry-run
    ;;
  machine-status)
    if [ -z "$target" ]; then echo "usage: $0 machine-status <host>" >&2; exit 2; fi
    echo "=== $target ==="
    ssh "$target" 'hostname; tmux ls 2>/dev/null || echo "no sessions"'
    ;;
  tmux-status)
    if [ -z "$target" ]; then echo "usage: $0 tmux-status <host>" >&2; exit 2; fi
    ssh "$target" 'tmux ls 2>/dev/null || echo "no sessions"'
    ;;
  attach-hint)
    if [ -z "$target" ] || [ -z "$session" ]; then
      echo "usage: $0 attach-hint <host> <session>" >&2
      exit 2
    fi
    echo "ssh $target"
    echo "tmux attach -t $session"
    ;;
  logs)
    log_session="${2:-}"
    log_pane="${3:-}"
    if [ -z "$log_session" ]; then echo "usage: $0 logs <session> [pane]" >&2; exit 2; fi
    case "$log_session" in
      openclaw-core) echo "tail -f $ROOT/logs/gateway_openclaw.log" ;;
      fleet-status)  echo "tail -f $ROOT/logs/fleet_orchestrator.log" ;;
      desk-pro)      echo "tail -f $ROOT/logs/desk_pro.log" ;;
      screeners)     echo "tail -f $ROOT/logs/screeners.log" ;;
      *)             echo "tail -f $ROOT/logs/${session}.log" ;;
    esac
    ;;
  health-all)
    cd "$ROOT"
    python3 scripts/tmux/health_check.py --summary 2>/dev/null || python3 scripts/tmux/health_check.py
    ;;
  *)
    echo "usage: $0 fleet-status|machine-status|tmux-status|attach-hint|logs|health-all [args...]" >&2
    exit 2
    ;;
esac
