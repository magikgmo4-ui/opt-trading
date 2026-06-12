#!/usr/bin/env bash
set -Eeuo pipefail
trap 'echo "[spacex_watch_loop] failed at line ${LINENO}" >&2' ERR

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "${ROOT_DIR}"
INTERVAL_SECONDS="${SPACEX_WATCH_INTERVAL_SECONDS:-600}"

echo "[spacex_watch_loop] monitor-only interval=${INTERVAL_SECONDS}s"
while true; do
  date -u +"[spacex_watch_loop] tick %Y-%m-%dT%H:%M:%SZ"
  bash scripts/ipo/spacex_collect_once.sh
  sleep "${INTERVAL_SECONDS}"
done
