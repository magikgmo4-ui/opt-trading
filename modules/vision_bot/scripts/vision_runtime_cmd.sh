#!/usr/bin/env bash
set -euo pipefail

SCRIPT_PATH="$(readlink -f "${BASH_SOURCE[0]}")"
SCRIPT_DIR="$(cd "$(dirname "$SCRIPT_PATH")" && pwd)"
BASE_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
REPO_ROOT="$(cd "$BASE_DIR/../.." && pwd)"

VISION_CMD="$BASE_DIR/scripts/vision_bot_cmd.sh"
VISION_SANITY="$BASE_DIR/scripts/vision_bot_sanity.sh"
STEP2_CMD="$REPO_ROOT/modules/bot_vision_step2/scripts/bot_vision_step2_cmd.sh"
STEP2_SANITY="$REPO_ROOT/modules/bot_vision_step2/scripts/bot_vision_step2_sanity.sh"

usage() {
  cat <<'EOF'
Usage: cmd-vision {sanity|paths|status|init|capture-once|analyze-latest|send-latest|prune-old|tail|menu}

Unified wrapper around the operational VISION pair:
  - vision_bot         (capture / inbox-outbox)
  - bot_vision_step2   (analysis / telegram / Desk Pro outputs)
EOF
}

cmd="${1:-help}"
shift || true

case "$cmd" in
  sanity)
    exec bash "$BASE_DIR/scripts/vision_runtime_sanity.sh"
    ;;

  paths)
    INBOX="${VISION_BOT_INBOX:-/srv/sftp/shared_files/shared/vision_inbox}"
    OUTBOX="${VISION_BOT_OUTBOX:-/srv/sftp/shared_files/shared/vision_outbox}"
    PROCESSED="${VISION_BOT_PROCESSED:-/srv/sftp/shared_files/shared/vision_processed}"
    cat <<EOF
VISION pair paths
  inbox      : $INBOX
  outbox     : $OUTBOX
  processed  : $PROCESSED

Scripts
  vision_bot        : $VISION_CMD
  bot_vision_step2  : $STEP2_CMD

Services / timers
  vision_bot.service
  bot_vision_step2.service
  bot_vision_step2_send.timer
  bot_vision_step2_prune.timer
EOF
    ;;

  status)
    echo "=== vision_bot.service ==="
    systemctl status vision_bot --no-pager || true
    echo
    echo "=== bot_vision_step2.service ==="
    bash "$STEP2_CMD" status || true
    echo
    echo "=== bot_vision_step2 timers ==="
    systemctl status bot_vision_step2_send.timer --no-pager || true
    systemctl status bot_vision_step2_prune.timer --no-pager || true
    ;;

  init)
    exec bash "$VISION_CMD" init
    ;;

  capture-once)
    exec bash "$VISION_CMD" run_once
    ;;

  analyze-latest)
    exec bash "$STEP2_CMD" analyze_latest "$@"
    ;;

  send-latest)
    exec bash "$STEP2_CMD" send_latest "$@"
    ;;

  prune-old)
    exec bash "$STEP2_CMD" prune_old "$@"
    ;;

  tail)
    echo "=== vision_bot journal ==="
    journalctl -u vision_bot -n 100 --no-pager || true
    echo
    echo "=== bot_vision_step2 journal ==="
    journalctl -u bot_vision_step2 -n 100 --no-pager || true
    ;;

  menu)
    exec bash "$BASE_DIR/scripts/vision_runtime_menu.sh"
    ;;

  help|-h|--help|"")
    usage
    ;;

  *)
    usage
    exit 1
    ;;
esac
