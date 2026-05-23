#!/bin/bash
set -euo pipefail
cd /opt/trading
DIFF=$(git diff --stat 2>&1)
echo "REPO_DIFF: $(echo "$DIFF" | tail -1)"
echo "$DIFF"
echo "{\"job\":\"repo-diff-check\",\"ts\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\",\"status\":\"PASS\"}" >> data/runtime_health/job_logs/ledger.jsonl
