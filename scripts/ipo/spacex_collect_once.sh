#!/usr/bin/env bash
set -Eeuo pipefail
trap 'echo "[spacex_collect_once] failed at line ${LINENO}" >&2' ERR

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "${ROOT_DIR}"

python3 -m modules.ipo_tracking.cli collect-once --offline-ok
python3 - <<'PY'
from modules.ipo_tracking.ui.spacex_page import write_static_page
print(write_static_page())
PY
