#!/usr/bin/env bash
set -Eeuo pipefail
trap 'echo "[spacex_report_daily] failed at line ${LINENO}" >&2' ERR

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "${ROOT_DIR}"
python3 -m modules.ipo_tracking.cli report
python3 -m modules.ipo_tracking.cli command-center \
  --json-out data/ipo/spacex/command_center/latest.json \
  --md-out reports/ipo/spacex/command_center_latest.md
