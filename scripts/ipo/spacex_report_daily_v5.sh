#!/usr/bin/env bash
set -Eeuo pipefail
trap 'echo "[spacex_report_daily_v5] failed at line ${LINENO}" >&2' ERR
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT_DIR"
python3 -m modules.ipo_tracking.cli report
