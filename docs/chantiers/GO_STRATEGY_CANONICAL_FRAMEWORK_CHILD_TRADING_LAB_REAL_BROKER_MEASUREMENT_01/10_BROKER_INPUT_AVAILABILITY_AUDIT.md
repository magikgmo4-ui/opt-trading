---
go_id: GO_STRATEGY_CANONICAL_FRAMEWORK_CHILD_TRADING_LAB_REAL_BROKER_MEASUREMENT_01
doc_type: audit
---

# Broker Input Availability Audit

## Résultat du check (2026-05-27)

```
state/trading_lab_v1/inputs/ : ABSENT
```

Aucun fichier CSV broker trouvé sous `state/trading_lab_v1/inputs/`. Ce répertoire n'existe pas encore.

## Contrat du fichier attendu

```
Chemin : state/trading_lab_v1/inputs/xauusd_m1_broker_<YYYYMMDD>.csv
Format  : CSV avec header
Colonnes requises :
  timestamp  — ISO 8601 avec timezone, ex: 2026-04-07T18:00:00-04:00
  open       — float, prix à l'ouverture
  high       — float, prix le plus haut
  low        — float, prix le plus bas
  close      — float, prix à la clôture
  volume     — float ou int (optionnel, 0 si absent)

Couverture minimale recommandée :
  ≥ 30 jours de données (sessions gold_open_18h + midnight_00h)
  ≥ 5 barres par session pour sequence_complete=true
  Inclure les barres post-session (18:05–18:10, 00:05–00:10) pour résolution TP/SL

Exemple de ligne valide :
  2026-04-07T18:00:00-04:00,3248.0,3250.5,3246.5,3249.5,120
```

## Instructions d'activation

```bash
# Placer le fichier (option A: données anonymisées)
cp /path/to/export_xauusd_m1.csv \
   state/trading_lab_v1/inputs/xauusd_m1_broker_20260407.csv

# Vérifier que state/ n'apparaît pas dans git status
git status  # ne doit PAS montrer state/

# Lancer le pipeline
python3 -c "
import sys; sys.path.insert(0, '.')
from modules.trading_lab_v1.app.trading_lab_v1 import run_with_outcomes
run_with_outcomes(['state/trading_lab_v1/inputs/xauusd_m1_broker_20260407.csv'])
"
```

## Verdict de ce check

`BLOCKED_NO_BROKER_INPUT` — aucune donnée broker disponible au moment du run de ce GO.
