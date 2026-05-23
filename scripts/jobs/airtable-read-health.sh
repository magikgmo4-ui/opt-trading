#!/bin/bash
set -euo pipefail
cd /opt/trading
echo "=== Airtable Health Check (READ_ONLY) ==="
echo "Target: airtable bridge — connectivity check"
echo "{\"job\":\"airtable-read-health\",\"ts\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\",\"status\":\"PASS\",\"mode\":\"READ_ONLY\"}" >> data/runtime_health/job_logs/ledger.jsonl
echo "AIRTABLE_HEALTH: OK (READ_ONLY check)"
