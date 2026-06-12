#!/usr/bin/env bash
set -Eeuo pipefail
trap 'echo "[spacex_watch_loop_v5] failed at line ${LINENO}" >&2' ERR
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT_DIR"
INTERVAL="${SPACEX_WATCH_INTERVAL_SECONDS:-600}"
while true; do
  python3 -m modules.ipo_tracking.cli collect-once || true
  sleep "$INTERVAL"
done
