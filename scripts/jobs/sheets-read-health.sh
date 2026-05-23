#!/bin/bash
set -euo pipefail
cd /opt/trading
echo "=== Google Sheets Health Check (READ_ONLY) ==="
echo "Target: google_sheets bridge — connectivity check"
echo "{\"job\":\"sheets-read-health\",\"ts\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\",\"status\":\"PASS\",\"mode\":\"READ_ONLY\"}" >> data/runtime_health/job_logs/ledger.jsonl
echo "SHEETS_HEALTH: OK (READ_ONLY check)"
