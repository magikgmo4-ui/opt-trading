#!/bin/bash
set -euo pipefail
cd /opt/trading
STATUS=$(git status --porcelain 2>&1)
echo "REPO_STATUS: $(echo "$STATUS" | wc -l) dirty files"
echo "$STATUS"
echo "{\"job\":\"repo-status-check\",\"ts\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\",\"status\":\"PASS\",\"dirty\":$(echo "$STATUS" | wc -l)}" >> data/runtime_health/job_logs/ledger.jsonl
