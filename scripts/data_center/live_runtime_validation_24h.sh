#!/usr/bin/env bash
# live_runtime_validation_24h.sh — 24h monitoring snapshot for Data Center
# Run every 4-6 hours, compare against baseline

set -euo pipefail
REPO=/opt/trading
cd "$REPO"
NOW=$(date -Iseconds)
REPORT="docs/chantiers/GO_OPT_TRADING_DATA_CENTER_CHILD_PRO_DESK_LIVE_RUNTIME_VALIDATION_01/runtime_snapshots/snapshot_$(date +%Y%m%d_%H%M%S).json"

mkdir -p "$(dirname "$REPORT")"

echo "=== Data Center Runtime Validation — $NOW ==="

# 1. Contract registry validator
echo "[1/6] Validator..."
VALID=$(venv/bin/python3 modules/data_center/contract_registry_validator.py --json 2>&1)
echo "$VALID" | python3 -c "import json,sys; d=json.load(sys.stdin); print('  valid:', d['valid'], '| errors:', len(d['errors']), '| contracts:', d['contracts_checked'])"

# 2. View freshness
echo "[2/6] Views freshness..."
venv/bin/python3 -c "
import json, os
from datetime import datetime, timezone
from pathlib import Path
views = Path('data/data_center/views')
fresh = 0; stale = 0; missing = 0; by_contract = {}
for d in sorted(views.iterdir()):
    if not d.is_dir(): continue
    latest = d / 'latest.json'
    if not latest.exists():
        by_contract[d.name] = {'status': 'MISSING'}; missing += 1; continue
    try:
        data = json.loads(latest.read_text())
        ts = data.get('produced_at','')
        freshness = data.get('freshness_state','')
        age = '?'
        if ts:
            try:
                dt = datetime.fromisoformat(ts.replace('Z','+00:00'))
                age_h = (datetime.now(timezone.utc) - dt).total_seconds() / 3600
                age = f'{age_h:.1f}h'
            except: pass
        if freshness == 'stale': stale += 1
        else: fresh += 1
        by_contract[d.name] = {'status': freshness, 'age': age}
    except: by_contract[d.name] = {'status': 'ERROR'}; missing += 1
print(f'  fresh={fresh} stale={stale} missing={missing}')
"

# 3. Pipeline hourly status
echo "[3/6] Pipeline..."
systemctl is-active collector-telegram-screener.timer 2>/dev/null && echo '  timer: active' || echo '  timer: INACTIVE'
systemctl is-active localcms 2>/dev/null && echo '  localcms: active' || echo '  localcms: INACTIVE'
systemctl is-active tv-webhook 2>/dev/null && echo '  webhook: active' || echo '  webhook: INACTIVE'
systemctl is-active tv-perf 2>/dev/null && echo '  perf: active' || echo '  perf: INACTIVE'

# 4. LocalCMS surfaces
echo "[4/6] LocalCMS..."
for ep in signals/summary backtest/summary vision/summary health; do
    code=$(curl -s -o /dev/null -w '%{http_code}' "http://localhost:8700/$ep" 2>/dev/null || echo '000')
    echo "  /$ep: $code"
done

# 5. Backtest
echo "[5/6] Backtest..."
BT=$(curl -s http://localhost:8700/backtest/summary 2>/dev/null | python3 -c "
import json,sys
d=json.load(sys.stdin)
gt=d.get('grand_total',{})
print(f\"  channels={gt.get('channels',0)} trades={gt.get('trades',0)} wr={gt.get('winrate_pct',0)}% avg_r={gt.get('avg_r',0)}\")
" 2>/dev/null || echo '  UNAVAILABLE')
echo "$BT"

# 6. Coverage
echo "[6/6] Coverage..."
venv/bin/python3 /tmp/show_coverage.py 2>&1 | grep "Sources:" 

echo "=== Done: $NOW ==="
