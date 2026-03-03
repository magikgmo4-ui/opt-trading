#!/usr/bin/env bash
set -euo pipefail
ACTION="${1:-help}"
shift || true

PY="/opt/trading/.venvs/bot_vision_step2/bin/python"
APP="/opt/trading/modules/bot_vision_step2/app/bot_vision_step2.py"

case "$ACTION" in
  sanity)
    "$PY" "$APP" sanity
    ;;
  analyze_latest)
    "$PY" "$APP" analyze_latest
    ;;
  send_latest)
    "$PY" "$APP" send_latest
    ;;
  prune_old)
    "$PY" "$APP" prune_old
    ;;
  serve)
    "$PY" "$APP" serve
    ;;
  status)
    sudo systemctl status bot_vision_step2 --no-pager || true
    ;;
  tail)
    sudo journalctl -u bot_vision_step2 -n 200 --no-pager || true
    ;;
  restart)
    sudo systemctl restart bot_vision_step2 || true
    ;;
  stop)
    sudo systemctl stop bot_vision_step2 || true
    ;;
  start)
    sudo systemctl start bot_vision_step2 || true
    ;;
  *)
    echo "Usage: cmd-bot_vision_step2 {sanity|analyze_latest|send_latest|prune_old|serve|status|tail|restart|stop|start}"
    exit 2
    ;;
esac
