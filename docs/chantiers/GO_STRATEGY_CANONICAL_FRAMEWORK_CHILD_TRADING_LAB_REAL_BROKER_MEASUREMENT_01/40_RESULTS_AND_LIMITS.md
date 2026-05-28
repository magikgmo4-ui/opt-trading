---
go_id: GO_STRATEGY_CANONICAL_FRAMEWORK_CHILD_TRADING_LAB_REAL_BROKER_MEASUREMENT_01
doc_type: results
---

# Résultats et limites

## Run effectué

**Statut : BLOCKED_NO_BROKER_INPUT**

Aucun fichier broker disponible au moment du run (2026-05-27).
`state/trading_lab_v1/inputs/` : absent.

## Résultats disponibles (données synthétiques de référence)

Source : `modules/trading_lab_v1/data/sample_xauusd_m1_real_like.csv` (92 rows)

```json
{
  "trades_count": 10,
  "win_count": 6,
  "loss_count": 4,
  "timeout_count": 0,
  "avg_r_realized": 0.8,
  "dates": ["2026-04-07", "2026-04-08", "2026-04-09", "2026-04-10", "2026-04-11", "2026-04-14"],
  "variants": {
    "xau_open_sweep_fvg": 3,
    "xau_open_no_sweep_no_fvg": 3,
    "xau_open_no_sweep_fvg": 2,
    "xau_open_sweep_no_fvg": 2
  }
}
```

Ces résultats sont sur données artificielles conçues pour produire des outcomes déterministes et ne reflètent pas la performance réelle de la stratégie.

## Limites

- `perf_status` reste `UNMEASURED` : données synthétiques insuffisantes pour décision
- Données broker réelles nécessaires (≥ 20 trades, spread ≥ 30 jours)
- Edge positif sur sample (avg_r=0.8) non représentatif : candles post-entrée ciblées

## Prochaine action requise

Placer un export XAUUSD M1 dans `state/trading_lab_v1/inputs/` et relancer ce GO.
