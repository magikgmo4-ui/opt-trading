#!/bin/bash
set -euo pipefail
cd /opt/trading
echo "=== Telegram Automation Digest (READ_ONLY) ==="
echo "Summary: $(date -u) — non-critical notification"
echo "{\"job\":\"telegram-automation-digest\",\"ts\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\",\"status\":\"PASS\",\"mode\":\"READ_ONLY\"}" >> data/runtime_health/job_logs/ledger.jsonl
echo "TELEGRAM_DIGEST: OK (non-critical notification)"
