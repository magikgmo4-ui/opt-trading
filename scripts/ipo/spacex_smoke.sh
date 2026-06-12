#!/usr/bin/env bash
set -Eeuo pipefail
trap 'echo "[spacex_smoke] failed at line ${LINENO}" >&2' ERR
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "${ROOT_DIR}"
python3 -m modules.ipo_tracking.cli smoke
test -f data/ipo/spacex/scored/latest_snapshot.json
test -f data/data_center/views/spacex_super_desk/latest.json
test -f ui/spacex_desk/index.html
echo "SPACEX_SMOKE_OK"
