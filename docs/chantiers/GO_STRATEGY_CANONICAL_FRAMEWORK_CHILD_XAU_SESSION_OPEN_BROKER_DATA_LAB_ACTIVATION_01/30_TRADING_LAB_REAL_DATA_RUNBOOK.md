---
doc_id: GO_STRATEGY_CANONICAL_FRAMEWORK_CHILD_XAU_SESSION_OPEN_BROKER_DATA_LAB_ACTIVATION_01_RUNBOOK
doc_type: runbook
go_id: GO_STRATEGY_CANONICAL_FRAMEWORK_CHILD_XAU_SESSION_OPEN_BROKER_DATA_LAB_ACTIVATION_01
---

# 30 — Runbook: activer trading_lab_v1 avec données réelles

## Étape 1 — Placer les données

```bash
# Option A: données anonymisées → committer dans data/
cp /path/to/xauusd_m1_export.csv \
   modules/trading_lab_v1/data/sample_xauusd_m1_real_like.csv

# Option B: données sensibles → ne pas committer (gitignorée)
mkdir -p state/trading_lab_v1/inputs/
cp /path/to/xauusd_m1_export.csv \
   state/trading_lab_v1/inputs/xauusd_m1_broker_<date>.csv
```

## Étape 2 — Lancer le lab sur un CSV externe

```python
# Depuis repo root (venv activé)
python3 -c "
import sys; sys.path.insert(0, '.')
from modules.trading_lab_v1.app.trading_lab_v1 import (
    load_profile, choose_session, process_market_run,
    load_market_csv, available_dates_for_session
)
from pathlib import Path

CSV_PATH = Path('modules/trading_lab_v1/data/sample_xauusd_m1_real_like.csv')
# Pour données broker: CSV_PATH = Path('state/trading_lab_v1/inputs/xauusd_m1_broker_<date>.csv')

profile = load_profile()
tz = profile['frame']['timezone']
rows = load_market_csv(CSV_PATH, tz)
print(f'Loaded {len(rows)} rows')

for session_id in ['gold_open_18h', 'midnight_00h']:
    session = choose_session(profile, session_id)
    dates = available_dates_for_session(rows, session)
    print(f'{session_id}: {len(dates)} dates available')
    for date in sorted(dates):
        result = process_market_run(profile, session, CSV_PATH, date)
        r = result['run_payload']
        print(f'  {date}: seq={r[\"sequence_complete\"]}, variant={r[\"variant_id\"]}, dir={r[\"direction\"]}')
"
```

## Étape 3 — Générer le batch report

```python
python3 modules/trading_lab_v1/app/trading_lab_v1.py batch-report
```

Ou pour une session spécifique:
```python
python3 modules/trading_lab_v1/app/trading_lab_v1.py batch-report gold_open_18h 2026-04-07 2026-04-14
```

## Étape 4 — Lire les résultats

```python
python3 -c "
import sys, json; sys.path.insert(0, '.')
from modules.trading_lab_v1.app.trading_lab_v1 import load_jsonl, TRADES_JSONL, FEATURES_JSONL
features = load_jsonl(FEATURES_JSONL)
trades = load_jsonl(TRADES_JSONL)
print(f'features: {len(features)}, trades: {len(trades)}')
variants = {}
for f in features:
    v = f.get('variant_id', 'none')
    variants[v] = variants.get(v, 0) + 1
print('variants:', variants)
"
```

## Exclure state/ du commit

```bash
# Vérifier que state/ est bien ignoré:
git status  # ne doit pas montrer state/trading_lab_v1/

# Si state/ apparaît accidentellement:
git rm -r --cached state/trading_lab_v1/ 2>/dev/null || true
# Et vérifier .gitignore contient bien: state/
```

## Tests

```bash
# Tests adapter
python3 -m pytest tests/test_strategy_adapter.py -q

# Tests trading_lab_v1
python3 -m pytest modules/trading_lab_v1/tests/ -q

# Registry validator
python3 tools/strategy/validate_strategy_registry.py
```
