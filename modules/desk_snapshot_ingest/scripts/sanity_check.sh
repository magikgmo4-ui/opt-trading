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
: "${INGEST_MODE:=move}"

echo "=== desk_snapshot_ingest sanity ==="
date -Iseconds
echo

command -v python3 >/dev/null && python3 --version || { echo "ERROR: python3 missing"; exit 1; }
[[ -x "$PY" ]] || { echo "ERROR: missing $PY"; exit 1; }

mkdir -p "$INBOX_DIR" "$DEST_DIR" "$PROCESSED_DIR" || true
test -w "$DEST_DIR" || { echo "ERROR: dest not writable: $DEST_DIR"; exit 1; }

python3 "$PY" --dry-run --inbox "$INBOX_DIR" --dest "$DEST_DIR" --index "$INDEX_FILE" --history "$HISTORY_FILE" --processed "$PROCESSED_DIR" --mode "$INGEST_MODE" >/dev/null
echo "PASS: sanity OK"
