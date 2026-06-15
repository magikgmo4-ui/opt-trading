#!/usr/bin/env bash
# Sync critical admin-trading runtime artifacts onto fantome.
set -euo pipefail

TRADING_ROOT="/opt/trading"
SRC_HOST="${FAILOVER_SRC_HOST:-admin-trading}"
BASE_DIR="$TRADING_ROOT/data/failover/admin-trading"
STATE_DIR="$BASE_DIR/state"
PERF_DIR="$BASE_DIR/perf"
SNAP_DIR="$BASE_DIR/shared_snapshots"
DESK_DIR="$SNAP_DIR/desk_pro_latest"
VISION_DIR="$SNAP_DIR/vision_outbox"
STAMP_FILE="$BASE_DIR/last_sync_utc.txt"

mkdir -p "$STATE_DIR" "$PERF_DIR" "$DESK_DIR" "$VISION_DIR"

echo "== admin failover sync =="
echo "source=$SRC_HOST"
echo "started_utc=$(date -u +%Y-%m-%dT%H:%M:%SZ)"

ssh -o BatchMode=yes -o ConnectTimeout=10 "$SRC_HOST" "hostname"

rsync -av "$SRC_HOST:/opt/trading/state/events.jsonl" "$STATE_DIR/"

# perf_app uses SQLite WAL; keep sidecar files together with the main DB.
rsync -av \
  --include='perf.db*' \
  --exclude='*' \
  "$SRC_HOST:/opt/trading/perf/" \
  "$PERF_DIR/"

rsync -av --delete \
  "$SRC_HOST:/srv/sftp/shared_files/shared/desk_pro/latest/" \
  "$DESK_DIR/"

rsync -av \
  "$SRC_HOST:/srv/sftp/shared_files/shared/vision_outbox/" \
  "$VISION_DIR/"

date -u +%Y-%m-%dT%H:%M:%SZ > "$STAMP_FILE"

echo "completed_utc=$(cat "$STAMP_FILE")"
ls -lh "${STATE_DIR}/events.jsonl"
ls -lh "$PERF_DIR"/perf.db*
ls -lh "$DESK_DIR"
tmp_listing="$(mktemp)"
find "$VISION_DIR" -maxdepth 1 -type f -printf '%TY-%Tm-%Td %TH:%TM %f\n' | sort -r > "$tmp_listing"
head -n 10 "$tmp_listing"
rm -f "$tmp_listing"
