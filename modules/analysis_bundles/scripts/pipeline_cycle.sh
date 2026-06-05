#!/usr/bin/env bash
# pipeline_cycle.sh — full automated cycle: sync → qualify → archive → verdict
# Runs every 30min via cron
set -euo pipefail
cd ~/opt-trading-clean

echo "[$(date -Is)] Pipeline cycle start"

# 1. Sync data from admin-trading
bash modules/analysis_bundles/scripts/sync_admin_trading.sh 2>&1 | tail -2

# 2. Live market metrics
python3 -c "from modules.analysis_bundles.app.market_metrics_writer import write_all; write_all()" 2>/dev/null

# 3. Batch qualify + archive signals
bash modules/analysis_bundles/scripts/batch_qualify.sh 2>&1 | tail -5

# 4. Archive signals for trading lab
python3 << 'PYEOF'
import sys; sys.path.insert(0, '.')
from modules.analysis_bundles.app.signal_tracker import archive_all_channels
r = archive_all_channels()
print(f"Archived: {r['total_signals']} signals, {len(r['channels'])} channels")
# Auto-promote channels >= 10 signals
for ch, info in r['channels'].items():
    if info['signals'] >= 10:
        print(f"  ACTIVE: {ch} ({info['signals']} signals) {info.get('assets', [])}")
PYEOF

# 5. Full pipeline verdict
python3 -m modules.analysis_bundles.app 2>/dev/null | head -5

echo "[$(date -Is)] Pipeline cycle done"
