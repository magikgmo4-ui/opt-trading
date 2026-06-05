---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_TV_TEST_RUNTIME_CONFIG_CANONICALIZE_01_40_VERIFY
doc_type: chantier/verification
repo: opt-trading
branch: go/GO_OPT_TRADING_ADMIN_TRADING_TV_TEST_RUNTIME_CONFIG_CANONICALIZE_01
machine: admin-trading
status: active
lifecycle_stage: config_canonicalize
---

# 40_VERIFICATION_PLAN — Plan de verification

## Verification locale (sur admin-trading)

### V1 : Presence du pattern

```bash
python3 -c "
import json
with open('/opt/trading/state/risk_config.json') as f:
    cfg = json.load(f)
accts = cfg.get('accounts', {})
assert 'TV_TEST' in accts, 'V1 FAIL: TV_TEST missing'
assert 'PAPER_TEST' in accts, 'V1: PAPER_TEST missing (non bloquant)'
print('V1 PASS: TV_TEST present')
"
```

### V2 : Valeurs valides

```bash
python3 -c "
import json
with open('/opt/trading/state/risk_config.json') as f:
    cfg = json.load(f)
tv = cfg['accounts']['TV_TEST']
assert tv['equity'] > 0, 'V2 FAIL: equity <= 0'
assert tv['risk_pct'] > 0, 'V2 FAIL: risk_pct <= 0'
assert tv['risk_pct'] <= 1.0, 'V2 FAIL: risk_pct > 1 (suspicious)'
print('V2 PASS: values valid')
"
```

### V3 : Risk quote fonctionnel

```bash
python3 -c "
import sys; sys.path.insert(0, '/opt/trading')
from webhook_server import risk_quote
q = risk_quote('TV_TEST', price=100.0, sl=95.0, tp=110.0)
assert q.get('qty', 0) > 0, 'V3 FAIL: qty <= 0'
assert q.get('risk_usd', 0) > 0, 'V3 FAIL: risk_usd <= 0'
print(f'V3 PASS: qty={q[\"qty\"]} risk_usd={q[\"risk_usd\"]}')
"
```

### V4 : No-trade inline

```bash
curl -sS http://127.0.0.1:8010/perf/open | python3 -c "
import json, sys
trades = json.load(sys.stdin).get('open', [])
tv = [t for t in trades if t.get('engine') == 'TV_TEST']
assert len(tv) == 0, 'V4 FAIL: TV_TEST trades found'
print('V4 PASS: 0 TV_TEST trades')
"
```

## Tableau de verification

| Check | Description | Critere |
| --- | --- | --- |
| V1 | TV_TEST present dans accounts | `assert 'TV_TEST' in accounts` |
| V2 | equity > 0, risk_pct > 0 | Valeurs valides |
| V3 | risk_quote() retourne qty > 0 | Quote fonctionnel |
| V4 | 0 TV_TEST trades | Perf ledger clean |

## RISKS

- À qualifier.
