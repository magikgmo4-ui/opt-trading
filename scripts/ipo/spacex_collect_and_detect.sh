#!/usr/bin/env bash
set -Eeuo pipefail
trap 'echo "[spacex_collect_and_detect] failed at line ${LINENO}" >&2' ERR
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT_DIR"

echo "=== SPCX V2 — collect + detect pipeline ==="

echo "--- [1/3] Running spacex collect-once ---"
bash scripts/ipo/spacex_collect_once_v5.sh --offline || echo "collect-once completed with warnings"

echo "--- [2/3] Running SPCX V2 setup detector ---"
python3 -m modules.spcx_v2.runner --once

echo "--- [3/3] SPCX V2 summary ---"
python3 -m modules.spcx_v2.runner --summary

echo "=== pipeline complete ==="
