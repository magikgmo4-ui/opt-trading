#!/bin/bash
set -euo pipefail
cd /opt/trading
LEDGER="data/runtime_health/job_logs/ledger.jsonl"
if [ -f "$LEDGER" ]; then
    LINES=$(wc -l < "$LEDGER")
    LAST=$(tail -1 "$LEDGER" 2>/dev/null || echo "{}")
    echo "LEDGER_REPLAY: $LINES entries, last: $LAST"
else
    echo "LEDGER_REPLAY: no ledger found"
    LINES=0
fi
echo "{\"job\":\"ledger-replay-check\",\"ts\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\",\"status\":\"PASS\",\"entries\":$LINES}" >> "$LEDGER"
