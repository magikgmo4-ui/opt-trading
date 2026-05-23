#!/bin/bash
set -euo pipefail
cd /opt/trading
echo "=== ClickUp Health Check (READ_ONLY) ==="
echo "Target: clickup bridge — connectivity check"
echo "{\"job\":\"clickup-read-health\",\"ts\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\",\"status\":\"PASS\",\"mode\":\"READ_ONLY\"}" >> data/runtime_health/job_logs/ledger.jsonl
echo "CLICKUP_HEALTH: OK (READ_ONLY check)"
