---
go_id: GO_STRATEGY_CANONICAL_FRAMEWORK_CHILD_TRADING_LAB_REAL_BROKER_MEASUREMENT_01
doc_type: runbook
---

# Runbook — mesure broker réelle

## Prérequis

1. Export XAUUSD M1 broker disponible (Dukascopy, MetaTrader, ou équivalent)
2. Format CSV conforme (voir `10_BROKER_INPUT_AVAILABILITY_AUDIT.md`)
3. Couverture ≥ 30 jours recommandée

## Étape 1 — Placer les données

```bash
mkdir -p state/trading_lab_v1/inputs/
cp /path/to/export.csv state/trading_lab_v1/inputs/xauusd_m1_broker_<YYYYMMDD>.csv

# Sécurité: vérifier que state/ est bien ignoré
git status  # ne doit PAS afficher state/
```

## Étape 2 — Run pipeline complet

```bash
python3 -c "
import sys, json
sys.path.insert(0, '.')
from modules.trading_lab_v1.app.trading_lab_v1 import run_with_outcomes
run_with_outcomes(['state/trading_lab_v1/inputs/xauusd_m1_broker_<YYYYMMDD>.csv'])
" 2>&1 | tee /tmp/lab_run_output.txt
```

## Étape 3 — Extraire les métriques du batch_report

```python
import sys, json
sys.path.insert(0, '.')
from modules.trading_lab_v1.app.trading_lab_v1 import load_jsonl, BATCH_REPORTS_JSONL
report = load_jsonl(BATCH_REPORTS_JSONL)[-1]
print(json.dumps({
    "trades_count": report["trades_count"],
    "win_count": report["win_count"],
    "loss_count": report["loss_count"],
    "timeout_count": report["timeout_count"],
    "avg_r_realized": report["avg_r_realized"],
    "dates": report["dates"],
    "variants": report["variants"],
}, indent=2))
```

## Étape 4 — Vérifier les tests

```bash
python3 tools/strategy/validate_strategy_registry.py
python3 -m pytest tests/test_strategy_adapter.py -q
python3 -m pytest modules/trading_lab_v1/tests/test_exit_outcome_v1.py -q
python3 -m pytest modules/trading_lab_v1/tests/test_pipeline_integration_v1.py -q
```

## Étape 5 — Documenter dans 40_RESULTS_AND_LIMITS.md

Copier la sortie du batch_report et noter:
- date du run
- fichier source (nom sans chemin sensible)
- métriques extraites
- verdict préliminaire

## Ne jamais faire

```bash
git add state/  # INTERDIT
git add -A      # risqué
git add .       # risqué
```
