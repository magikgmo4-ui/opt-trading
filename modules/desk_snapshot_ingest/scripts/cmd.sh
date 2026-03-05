#!/usr/bin/env bash
set -euo pipefail

SCRIPT="${BASH_SOURCE[0]}"
if command -v readlink >/dev/null 2>&1; then
  SCRIPT="$(readlink -f "$SCRIPT" 2>/dev/null || echo "$SCRIPT")"
fi
BASE="$(cd "$(dirname "$SCRIPT")/.." && pwd)"
PY="$BASE/ingest_snapshots.py"

: "${INBOX_DIR:=/srv/sftp/shared_files/shared/inbox}"
: "${DEST_DIR:=/opt/trading/desk/snapshots}"
: "${INDEX_FILE:=/opt/trading/desk/snapshots/latest.json}"
: "${HISTORY_FILE:=/opt/trading/desk/snapshots/history.jsonl}"
: "${PROCESSED_DIR:=/srv/sftp/shared_files/shared/inbox/_processed}"
: "${INGEST_MODE:=move}"  # move|copy

usage() {
  cat <<USAGE
desk_snapshot_ingest cmd

Usage:
  $0 ingest_once
  $0 ingest_watch [interval_seconds]
  $0 show_latest
  $0 tail_history
  $0 print_config
  $0 install_shortcuts  (sudo)
USAGE
}

ingest_once() {
  "$PY" --inbox "$INBOX_DIR" --dest "$DEST_DIR" --index "$INDEX_FILE" --history "$HISTORY_FILE" --processed "$PROCESSED_DIR" --mode "$INGEST_MODE"
}

ingest_watch() {
  local interval="${1:-3}"
  "$PY" --watch --interval "$interval" --inbox "$INBOX_DIR" --dest "$DEST_DIR" --index "$INDEX_FILE" --history "$HISTORY_FILE" --processed "$PROCESSED_DIR" --mode "$INGEST_MODE"
}

show_latest() { [[ -f "$INDEX_FILE" ]] && sed -n '1,220p' "$INDEX_FILE" || echo "No index: $INDEX_FILE"; }
tail_history() { [[ -f "$HISTORY_FILE" ]] && tail -n 80 "$HISTORY_FILE" || echo "No history: $HISTORY_FILE"; }

print_config() {
  cat <<CFG
BASE=$BASE
PY=$PY
INBOX_DIR=$INBOX_DIR
DEST_DIR=$DEST_DIR
INDEX_FILE=$INDEX_FILE
HISTORY_FILE=$HISTORY_FILE
PROCESSED_DIR=$PROCESSED_DIR
INGEST_MODE=$INGEST_MODE
CFG
}

install_shortcuts() { sudo "$BASE/scripts/install_shortcuts.sh"; }

cmd="${1:-}"; shift || true
case "$cmd" in
  ingest_once) ingest_once ;;
  ingest_watch) ingest_watch "${1:-3}" ;;
  show_latest) show_latest ;;
  tail_history) tail_history ;;
  print_config) print_config ;;
  install_shortcuts) install_shortcuts ;;
  ""|-h|--help|help) usage ;;
  *) echo "Unknown cmd: $cmd"; usage; exit 2 ;;
esac
