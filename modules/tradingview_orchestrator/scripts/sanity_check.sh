#!/usr/bin/env bash
set -euo pipefail

MOD="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PASS=0; FAIL=0

check() {
  local label="$1"; local cmd="$2"
  if eval "$cmd" &>/dev/null; then
    echo "  PASS  $label"
    ((PASS++)) || true
  else
    echo "  FAIL  $label"
    ((FAIL++)) || true
  fi
}

echo "=== tradingview_orchestrator sanity ==="

check "python3 available"     "command -v python3"
check "ssh cursor-ai reachable" "ssh -o BatchMode=yes -o ConnectTimeout=5 cursor-ai 'exit 0'"
check "tv_runner.py exists"   "test -f '$MOD/app/tv_runner.py'"
check "schemas/tv_job_v1.json" "test -f '$MOD/../../schemas/tv_job_v1.json'"
check "reports/tradingview dir (or can create)" "mkdir -p '$MOD/../../reports/tradingview'"
check "cursor-ai opt-trading path" \
  "ssh -o BatchMode=yes -o ConnectTimeout=10 cursor-ai 'powershell -NoProfile -NonInteractive -Command \"Test-Path \\\"C:\\\\Users\\\\ghost\\\\opt-trading\\\\modules\\\\tradingview_observer\\\"\"'"
check "cursor-ai tradingview-mcp CLI" \
  "ssh -o BatchMode=yes -o ConnectTimeout=10 cursor-ai 'powershell -NoProfile -NonInteractive -Command \"Test-Path \\\"C:\\\\Users\\\\ghost\\\\.claude\\\\tools\\\\tradingview-mcp\\\\src\\\\cli\\\\index.js\\\"\"'"

echo ""
echo "PASS=$PASS  FAIL=$FAIL"
[[ $FAIL -eq 0 ]] && exit 0 || exit 1
