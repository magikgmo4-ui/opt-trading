---
go_id: GO_STRATEGY_CANONICAL_FRAMEWORK_CHILD_TRADING_LAB_REAL_BROKER_MEASUREMENT_01
doc_type: contract
---

# Contrat de mesure broker réelle

## Commande

```bash
python3 -c "
import sys; sys.path.insert(0, '.')
from modules.trading_lab_v1.app.trading_lab_v1 import run_with_outcomes
run_with_outcomes(['state/trading_lab_v1/inputs/xauusd_m1_broker_<date>.csv'])
"
```

## Métriques à extraire du batch_report

| Métrique | Champ | Seuil minimum pour décision |
|---|---|---|
| Sessions traitées | `trades_count` | ≥ 20 |
| Win rate | `win_count / trades_count` | indicatif |
| Loss rate | `loss_count / trades_count` | indicatif |
| Timeout rate | `timeout_count / trades_count` | < 30% = données suffisantes |
| R moyen réalisé | `avg_r_realized` | > 0 = edge positif |
| Variants couverts | `variants` | 4/4 = couverture complète |
| Dates | `dates` | spread temporel |

## Promotion perf_status

`perf_status` dans le registry reste `UNMEASURED` jusqu'à :
- ≥ 20 trades sur données broker réelles
- spread temporel ≥ 30 jours
- timeout_count / total < 30%

## Sécurité données

- `state/` est gitignored — aucun fichier broker ne peut être commité accidentellement
- Vérifier `git status` avant tout commit
- Ne jamais utiliser `git add -A` ou `git add .` pour ce GO
