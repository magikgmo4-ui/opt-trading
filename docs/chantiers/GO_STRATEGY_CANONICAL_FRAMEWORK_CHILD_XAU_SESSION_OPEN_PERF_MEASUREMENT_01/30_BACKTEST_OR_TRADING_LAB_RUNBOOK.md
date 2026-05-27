---
doc_id: GO_STRATEGY_CANONICAL_FRAMEWORK_CHILD_XAU_SESSION_OPEN_PERF_MEASUREMENT_01_RUNBOOK
doc_type: runbook
go_id: GO_STRATEGY_CANONICAL_FRAMEWORK_CHILD_XAU_SESSION_OPEN_PERF_MEASUREMENT_01
---

# 30 — Runbook trading_lab_v1 — xau_session_open_v1

## Exécution sur sample data (reproductible)

```python
# Depuis la racine du repo (venv activé)
python3 -c "
import sys; sys.path.insert(0, '.')
from modules.trading_lab_v1.app.trading_lab_v1 import (
    load_profile, choose_session, process_market_run, load_jsonl,
    SAMPLE_MARKET_CSV, EVENTS_JSONL, TRADES_JSONL, FEATURES_JSONL,
    load_market_csv, available_dates_for_session
)

profile = load_profile()
tz = profile['frame']['timezone']
rows = load_market_csv(SAMPLE_MARKET_CSV, tz)

for session_id in ['gold_open_18h', 'midnight_00h']:
    session = choose_session(profile, session_id)
    dates = available_dates_for_session(rows, session)
    for date in dates:
        result = process_market_run(profile, session, SAMPLE_MARKET_CSV, date)
        r = result['run_payload']
        t = result['trade']
        print(f'{session_id} {date}: seq={r[\"sequence_complete\"]}, variant={r[\"variant_id\"]}')
"
```

## Batch report (après au moins un run)

```bash
python3 modules/trading_lab_v1/app/trading_lab_v1.py batch-report
```

## Exécution avec données réelles futures

```bash
# Remplacer le CSV par un export broker (format: timestamp,open,high,low,close,volume)
python3 -c "
from modules.trading_lab_v1.app.trading_lab_v1 import (
    load_profile, choose_session, process_market_run,
    load_market_csv, available_dates_for_session
)
from pathlib import Path

profile = load_profile()
csv_path = Path('/path/to/real/xauusd_m1_data.csv')
tz = profile['frame']['timezone']
rows = load_market_csv(csv_path, tz)

for session_id in ['gold_open_18h', 'midnight_00h']:
    session = choose_session(profile, session_id)
    for date in available_dates_for_session(rows, session):
        process_market_run(profile, session, csv_path, date)
"
```

## Tests

```bash
# Adapter tests
python3 -m pytest tests/test_strategy_adapter.py -q

# Trading lab readonly test (pre-existing failures documentées hors scope ce GO)
python3 -m pytest modules/trading_lab_v1/tests/test_strategy_id_adapter_readonly.py -q

# Registry validator
python3 tools/strategy/validate_strategy_registry.py
```

## Notes

- `state/trading_lab_v1/` est créé automatiquement par le lab au premier run
- Les fichiers `.jsonl` dans `state/` sont des données volatiles — ne pas committer
- Le sample CSV `modules/trading_lab_v1/data/sample_xauusd_m1.csv` est synthétique (12 lignes)
