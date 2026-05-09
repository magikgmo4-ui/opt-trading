#!/bin/bash
set -Eeuo pipefail

DRY_RUN_MODE="${DRY_RUN_MODE:-true}"

cd /opt/trading

PYTHONPATH=/opt/trading python -c "
from modules.desk_pro.dry_run import run_desk_pro_dry_run

import json

signal_event = {
    'event_type': 'signal',
    'symbol': 'BTCUSDT',
    'timeframe': '1h',
    'direction': 'long',
    'source': 'timer_trigger',
}

result = run_desk_pro_dry_run(signal_event)

print(json.dumps(result, indent=2, default=str))
"

echo "PASS: dry-run completed"