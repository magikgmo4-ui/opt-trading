#!/bin/bash
set -euo pipefail
cd /opt/trading
python3 scripts/ai/workers/strict_worker_denied_command_scan.py 2>&1
echo "---"
python3 scripts/ai/tests/g05_strict_worker_e2e_readonly.py 2>&1
echo "{\"job\":\"anti-leak-scan\",\"ts\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\",\"status\":\"PASS\"}" >> data/runtime_health/job_logs/ledger.jsonl
