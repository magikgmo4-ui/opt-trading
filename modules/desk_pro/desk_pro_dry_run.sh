#!/bin/bash
set -Eeuo pipefail

DRY_RUN_MODE="${DRY_RUN_MODE:-true}"

cd /opt/trading

PYTHONPATH=/opt/trading python -c "
from datetime import datetime, timezone

from modules.desk_pro.dry_run import run_desk_pro_dry_run

import json

signal_event = {
    'engine': 'DESK_PRO_TIMER',
    'signal': 'BUY',
    'symbol': 'BTCUSDT',
    'tf': 'H1',
    '_ts': datetime.now(timezone.utc).isoformat(),
}

result = run_desk_pro_dry_run(signal_event)

print(json.dumps(result, indent=2, default=str))
"

echo "PASS: dry-run completed"
