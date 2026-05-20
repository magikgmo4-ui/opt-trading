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
    ssh -o BatchMode=yes -o ConnectTimeout=5 "$target" 'hostname; tmux ls 2>/dev/null || echo "no sessions"'
    echo "--- fleet_status ---"
    python3 -c "
import json, sys
try:
    with open('${ROOT}/data/runtime_health/fleet_status.json') as f:
        d = json.load(f)
    entry = d.get('machines', {}).get('${target}', {})
    if entry:
        print('  status:     ', entry.get('overall_status', 'unknown'))
        print('  stale:      ', entry.get('stale', False))
        print('  age_minutes:', round(float(entry.get('age_minutes', 0) or 0), 1))
    else:
        print('  no fleet_status entry for ${target}')
except Exception as e:
    print('  fleet_status unavailable:', e)
" 2>/dev/null || echo "  fleet_status unavailable"
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
    if [ -z "$log_session" ]; then echo "usage: $0 logs <session>" >&2; exit 2; fi
    case "$log_session" in
      openclaw-core) echo "tail -f $ROOT/logs/gateway_openclaw.log" ;;
      fleet-status)  echo "tail -f $ROOT/logs/fleet_orchestrator.log" ;;
      desk-pro)      echo "tail -f $ROOT/logs/desk_pro.log" ;;
      screeners)     echo "tail -f $ROOT/logs/screeners.log" ;;
      *)             echo "tail -f $ROOT/logs/${log_session}.log" ;;
    esac
    ;;
  session-logs)
    # Show last N lines from a session log. Optional host for SSH multi-machine.
    # Usage: session-logs <session> [N=50] [host]
    log_session="${2:-}"
    lines="${3:-50}"
    remote_host="${4:-}"
    if [ -z "$log_session" ]; then
      echo "usage: $0 session-logs <session> [N=50] [host]" >&2
      exit 2
    fi
    case "$log_session" in
      openclaw-core) log_file="gateway_openclaw.log" ;;
      fleet-status)  log_file="fleet_orchestrator.log" ;;
      desk-pro)      log_file="desk_pro.log" ;;
      screeners)     log_file="screeners.log" ;;
      *)             log_file="${log_session}.log" ;;
    esac
    if [ -n "$remote_host" ]; then
      ssh -o BatchMode=yes -o ConnectTimeout=5 "$remote_host" \
        "tail -n ${lines} /opt/trading/logs/${log_file} 2>/dev/null || echo 'log not found: /opt/trading/logs/${log_file}'"
    else
      log_path="$ROOT/logs/$log_file"
      if [ -f "$log_path" ]; then
        tail -n "$lines" "$log_path"
      else
        echo "no log at $log_path" >&2
        exit 1
      fi
    fi
    ;;
  health-all)
    cd "$ROOT"
    python3 scripts/tmux/health_check.py --summary 2>/dev/null || python3 scripts/tmux/health_check.py
    ;;
  health-aggregate)
    dry_run_flag=""
    if [ "${2:-}" = "--dry-run" ]; then dry_run_flag="--dry-run"; fi
    cd "$ROOT"
    python3 modules/openclaw_tmux_operator/scripts/health_aggregate.py $dry_run_flag
    ;;
  openclaw-health)
    host="${2:-db-layer}"
    ssh -o BatchMode=yes -o ConnectTimeout=5 "$host" \
      "bash /opt/trading/modules/gateway_openclaw/scripts/cmd.sh health 2>&1 || echo 'openclaw health unavailable'"
    ;;
  openclaw-probe)
    host="${2:-db-layer}"
    ssh -o BatchMode=yes -o ConnectTimeout=5 "$host" \
      "bash /opt/trading/modules/gateway_openclaw/scripts/cmd.sh probe 2>&1 || echo 'openclaw probe unavailable'"
    ;;
  *)
    cat >&2 <<'USAGE'
usage: cmd.sh <command> [args...]

Read-only status / health / log commands:
  fleet-status                          fleet_orchestrator dry-run (local)
  machine-status  <host>                hostname + tmux ls + fleet_status JSON
  tmux-status     <host>                tmux ls via SSH
  attach-hint     <host> <session>      print SSH + attach command
  logs            <session>             print tail -f hint for session log
  session-logs    <session> [N=50]      last N lines of session log (local)
  session-logs    <session> [N=50] <host>  last N lines via SSH (remote)
  health-all                            tmux health_check.py (local)
  health-aggregate [--dry-run]          multi-machine tmux + health + fleet aggregation
  openclaw-health  [host=db-layer]      OpenClaw gateway health via SSH
  openclaw-probe   [host=db-layer]      OpenClaw gateway probe via SSH
USAGE
    exit 2
    ;;
esac
