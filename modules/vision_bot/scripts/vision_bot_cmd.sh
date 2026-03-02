#!/usr/bin/env bash
set -euo pipefail

SCRIPT_PATH="$(readlink -f "${BASH_SOURCE[0]}")"
SCRIPT_DIR="$(cd "$(dirname "$SCRIPT_PATH")" && pwd)"
BASE_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
APP="$BASE_DIR/app/vision_bot.py"

cmd="${1:-menu}"
shift || true

case "$cmd" in
  sanity)
    bash "$BASE_DIR/scripts/vision_bot_sanity.sh"
    ;;
  init)
    INBOX="${VISION_BOT_INBOX:-/srv/sftp/shared_files/shared/vision_inbox}"
    OUTBOX="${VISION_BOT_OUTBOX:-/srv/sftp/shared_files/shared/vision_outbox}"
    PROCESSED="${VISION_BOT_PROCESSED:-/srv/sftp/shared_files/shared/vision_processed}"
    mkdir -p "$INBOX" "$OUTBOX" "$PROCESSED"
    echo "OK: init dirs"
    echo " inbox=$INBOX"
    echo " outbox=$OUTBOX"
    echo " processed=$PROCESSED"
    ;;
  run_once)
    python3 "$APP" run_once
    ;;
  watch)
    REPO_ROOT="$(cd "$BASE_DIR/../.." && pwd)"
    WORKDIR="${VISION_BOT_WORKDIR:-$REPO_ROOT/_work/vision_bot}"
    LOG="${VISION_BOT_LOG:-$WORKDIR/vision_bot.log}"
    PIDFILE="$WORKDIR/vision_bot.pid"
    mkdir -p "$WORKDIR"
    if [[ -f "$PIDFILE" ]] && kill -0 "$(cat "$PIDFILE")" 2>/dev/null; then
      echo "ERR: already running pid=$(cat "$PIDFILE")"
      exit 1
    fi
    nohup python3 "$APP" watch >>"$LOG" 2>&1 &
    echo $! >"$PIDFILE"
    echo "OK: started watch pid=$(cat "$PIDFILE")"
    echo "log=$LOG"
    ;;
  stop)
    REPO_ROOT="$(cd "$BASE_DIR/../.." && pwd)"
    WORKDIR="${VISION_BOT_WORKDIR:-$REPO_ROOT/_work/vision_bot}"
    PIDFILE="$WORKDIR/vision_bot.pid"
    if [[ -f "$PIDFILE" ]]; then
      pid="$(cat "$PIDFILE")"
      if kill -0 "$pid" 2>/dev/null; then
        kill "$pid"
        echo "OK: stopped pid=$pid"
      else
        echo "WARN: pid not running: $pid"
      fi
      rm -f "$PIDFILE"
    else
      echo "WARN: no pidfile"
    fi
    ;;
  tail)
    REPO_ROOT="$(cd "$BASE_DIR/../.." && pwd)"
    WORKDIR="${VISION_BOT_WORKDIR:-$REPO_ROOT/_work/vision_bot}"
    LOG="${VISION_BOT_LOG:-$WORKDIR/vision_bot.log}"
    mkdir -p "$WORKDIR"
    touch "$LOG"
    tail -n 200 -f "$LOG"
    ;;
  menu)
    bash "$BASE_DIR/scripts/vision_bot_menu.sh"
    ;;
  *)
    echo "Usage: cmd-vision_bot {sanity|init|run_once|watch|stop|tail|menu}"
    exit 2
    ;;
esac
