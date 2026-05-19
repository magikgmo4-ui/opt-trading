#!/usr/bin/env bash
set -euo pipefail
BASE="$(cd "$(dirname "$0")/.." && pwd)"

usage() {
  cat <<'EOF'
Usage: cmd.sh <command>

Commands:
  print_config    Show config (if present)
  dry_run         Show what would be pruned
  prune_now       Prune now
  install_timer   Install systemd timer (every 10 minutes)
  status_timer    Show timer status
  uninstall_timer Remove timer/service
EOF
}

CMD="${1:-}"
[ -z "$CMD" ] && { usage; exit 1; }

CFG="$BASE/config/desk_retention.env"
case "$CMD" in
  print_config)
    [ -f "$CFG" ] && sed -n '1,220p' "$CFG" || { echo "No config at $CFG"; exit 2; }
    ;;
  dry_run)   bash "$BASE/desk_retention.sh" 1 ;;
  prune_now) bash "$BASE/desk_retention.sh" 0 ;;
  install_timer)
    sudo install -m 0644 "$BASE/systemd/desk_retention.service" /etc/systemd/system/desk_retention.service
    sudo install -m 0644 "$BASE/systemd/desk_retention.timer" /etc/systemd/system/desk_retention.timer
    sudo systemctl daemon-reload
    sudo systemctl enable --now desk_retention.timer
    echo "OK: installed+enabled desk_retention.timer"
    ;;
  status_timer)
    systemctl status desk_retention.timer --no-pager || true
    systemctl list-timers --all | grep -E 'desk_retention' || true
    ;;
  uninstall_timer)
    sudo systemctl disable --now desk_retention.timer || true
    sudo rm -f /etc/systemd/system/desk_retention.timer /etc/systemd/system/desk_retention.service
    sudo systemctl daemon-reload
    echo "OK: removed desk_retention timer/service"
    ;;
  *) echo "Unknown: $CMD"; usage; exit 1 ;;
esac
