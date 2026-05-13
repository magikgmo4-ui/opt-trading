#!/bin/bash
set -Eeuo pipefail

DRY_RUN_MODE="${DRY_RUN_MODE:-true}"
DESK_PRO_DRY_RUN_OUTPUT_DIR="${DESK_PRO_DRY_RUN_OUTPUT_DIR:-/opt/trading/runtime/desk_pro_dry_run}"
DESK_PRO_DRY_RUN_DESK_SNAPSHOT_PATH="${DESK_PRO_DRY_RUN_DESK_SNAPSHOT_PATH:-/opt/trading/desk/snapshots/latest.json}"

cd /opt/trading

PYTHONPATH=/opt/trading python -c "
from datetime import datetime, timezone

from modules.desk_pro.dry_run import (
    load_latest_desk_snapshot,
    run_desk_pro_dry_run,
    write_desk_pro_dry_run_artifacts,
)

import json
import os

signal_event = {
    'engine': 'DESK_PRO_TIMER',
    'signal': 'BUY',
    'symbol': 'BTCUSDT',
    'tf': 'H1',
    '_ts': datetime.now(timezone.utc).isoformat(),
}

snapshot_path = os.environ.get('DESK_PRO_DRY_RUN_DESK_SNAPSHOT_PATH', '/opt/trading/desk/snapshots/latest.json')
desk_snapshot = load_latest_desk_snapshot(snapshot_path, target_symbol='BTCUSDT')

result = run_desk_pro_dry_run(signal_event, desk_snapshot=desk_snapshot)

output_dir = os.environ.get('DESK_PRO_DRY_RUN_OUTPUT_DIR', '/opt/trading/runtime/desk_pro_dry_run')
artifact_meta = write_desk_pro_dry_run_artifacts(result, output_dir)
result['artifact_meta'] = artifact_meta

print(json.dumps(result, indent=2, default=str))
"

echo "PASS: dry-run completed"
