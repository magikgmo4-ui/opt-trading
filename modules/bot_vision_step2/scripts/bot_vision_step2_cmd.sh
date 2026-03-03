#!/usr/bin/env bash
set -euo pipefail

# bot_vision_step2 cmd wrapper
# - Works on admin-trading (where the venv + systemd unit exist)
# - Also works on student (where we usually DON'T install the venv nor the systemd unit):
#   * sanity works (no venv needed)
#   * service commands show a helpful message if unit doesn't exist
#   * runtime commands error clearly if venv missing

BASE="/opt/trading/modules/bot_vision_step2"
VENV_PY="/opt/trading/.venvs/bot_vision_step2/bin/python"

usage() {
  echo "Usage: cmd-bot_vision_step2 {sanity|analyze_latest|send_latest|prune_old|serve|status|tail|restart|stop|start}"
}

need_venv() {
  if [[ ! -x "$VENV_PY" ]]; then
    echo "ERR: bot_vision_step2 venv missing: $VENV_PY" >&2
    echo "     This is expected on machines like 'student' (archivist)." >&2
    echo "     Install only on the machine that runs the bot (admin-trading):" >&2
    echo "       sudo bash $BASE/scripts/install_service.sh" >&2
    exit 2
  fi
}

cmd="${1:-}"
shift || true

case "$cmd" in
  sanity)
    # sanity is designed to be portable (can PASS with warnings on student)
    exec bash "$BASE/scripts/bot_vision_step2_sanity.sh"
    ;;

  analyze_latest|send_latest|prune_old|serve)
    need_venv
    exec "$VENV_PY" "$BASE/app/bot_vision_step2.py" "$cmd" "$@"
    ;;

  status)
    # no sudo needed; on student it may say "unit not found" (expected)
    systemctl status bot_vision_step2 --no-pager || true
    ;;

  tail)
    journalctl -u bot_vision_step2 -n 200 --no-pager || true
    ;;

  restart)
    sudo systemctl restart bot_vision_step2
    ;;

  stop)
    sudo systemctl stop bot_vision_step2
    ;;

  start)
    sudo systemctl start bot_vision_step2
    ;;

  ""|-h|--help|help)
    usage
    exit 0
    ;;

  *)
    usage
    exit 1
    ;;
esac
