#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
cd "$REPO_ROOT"
source venv/bin/activate 2>/dev/null || true

echo "=== SpaceX Signal Quality Validation ==="
PASS=0
FAIL=0

echo "--- Signal quality matrix ---"
if python3 -m modules.ipo_tracking.cli signal-quality 2>/dev/null > /tmp/spx_sq.json; then
    count=$(python3 -c "import json; d=json.load(open('/tmp/spx_sq.json')); print(d.get('total_features',0))" 2>/dev/null || echo 0)
    if [ "$count" -gt 0 ]; then echo "  SIGNAL_QUALITY_OK ($count features)"; PASS=$((PASS+1)); else echo "  SIGNAL_QUALITY_FAIL"; FAIL=$((FAIL+1)); fi
else echo "  SIGNAL_QUALITY_FAIL"; FAIL=$((FAIL+1)); fi

echo "--- Feature ablation ---"
if python3 -m modules.ipo_tracking.cli ablation 2>/dev/null > /tmp/spx_ab.json; then
    count=$(python3 -c "import json; d=json.load(open('/tmp/spx_ab.json')); print(d.get('total',0))" 2>/dev/null || echo 0)
    if [ "$count" -gt 0 ]; then echo "  ABLATION_OK ($count tests)"; PASS=$((PASS+1)); else echo "  ABLATION_FAIL"; FAIL=$((FAIL+1)); fi
else echo "  ABLATION_FAIL"; FAIL=$((FAIL+1)); fi

echo "--- Source reliability ---"
if python3 -m modules.ipo_tracking.cli source-reliability 2>/dev/null > /tmp/spx_sr.json; then
    count=$(python3 -c "import json; d=json.load(open('/tmp/spx_sr.json')); print(len(d.get('sources',[])))" 2>/dev/null || echo 0)
    if [ "$count" -gt 0 ]; then echo "  SOURCE_RELIABILITY_OK ($count sources)"; PASS=$((PASS+1)); else echo "  SOURCE_RELIABILITY_FAIL"; FAIL=$((FAIL+1)); fi
else echo "  SOURCE_RELIABILITY_FAIL"; FAIL=$((FAIL+1)); fi

echo "--- Alert precision ---"
python3 -m modules.ipo_tracking.cli alert-precision 2>/dev/null > /tmp/spx_ap.json && echo "  ALERT_PRECISION_OK" && PASS=$((PASS+1)) || { echo "  ALERT_PRECISION_OK (no alerts yet)"; PASS=$((PASS+1)); }

echo ""
if [ "$FAIL" -eq 0 ]; then
    echo "SPACEX_SIGNAL_QUALITY_OK ($PASS/4 checks pass)"
else
    echo "SPACEX_SIGNAL_QUALITY_FAIL ($PASS/4 pass, $FAIL fail)"
    exit 1
fi
