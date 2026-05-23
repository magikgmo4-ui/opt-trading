#!/bin/bash
set -euo pipefail
mkdir -p data/runtime_health/job_logs
echo "{\"job\":\"ledger-heartbeat\",\"ts\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\",\"status\":\"PASS\"}" >> data/runtime_health/job_logs/ledger.jsonl
echo "LEDGER_HEARTBEAT: OK $(date -u)"
