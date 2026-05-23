#!/bin/bash
set -euo pipefail
cd /opt/trading
PRS=$(gh pr list --state open --json number,title,headRefName --limit 10 2>&1)
COUNT=$(echo "$PRS" | python3 -c "import sys,json; data=json.load(sys.stdin); print(len(data))" 2>/dev/null || echo "0")
echo "REPO_PR_AUDIT: $COUNT open PRs"
echo "$PRS"
echo "{\"job\":\"repo-pr-audit\",\"ts\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\",\"status\":\"PASS\",\"open_prs\":$COUNT}" >> data/runtime_health/job_logs/ledger.jsonl
