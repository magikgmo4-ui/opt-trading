---
go_id: GO_STRATEGY_CANONICAL_FRAMEWORK_CHILD_TRADING_LAB_DUKASCOPY_M1_COLLECTOR_01
doc_type: results
---

# Résultats et limites

## Smoke test collecteur

```
Source  : Dukascopy public datafeed
Symbol  : XAUUSD
Range   : 2026-04-07 → 2026-04-11 UTC (6 jours UTC incluant +1 pour midnight ET)
Fichier : state/trading_lab_v1/inputs/xauusd_m1_broker_20260407_20260411.csv
Rows    : 8640
Days fetched : 6, days_empty : 0
First ts : 2026-04-06T20:00:00-04:00
Last ts  : 2026-04-12T19:59:00-04:00
```

Prix réels XAUUSD sur cette période : ~4650–4850 USD/oz

## Pipeline run-with-outcomes sur données réelles

```json
{
  "runs_done": 12,
  "resolved": 12,
  "wins": 1,
  "losses": 9,
  "timeouts": 2,
  "avg_r_realized": -0.7,
  "dates": ["2026-04-07","2026-04-08","2026-04-09","2026-04-10","2026-04-11","2026-04-12"],
  "variants": {
    "xau_open_no_sweep_no_fvg": 5,
    "xau_open_sweep_fvg": 1,
    "xau_open_sweep_no_fvg": 6
  },
  "directions": {"bullish": 6, "bearish": 2, "neutral": 4}
}
```

## Observations

- **4 sessions neutral** : `first5_body_delta ≈ 0` sur cette semaine volatile → direction indéterminée. Ces trades `neutral` sont générés mais la stratégie nécessite un audit de l'impact des neutrals sur les outcomes.
- **2 timeouts** : barres post-entrée insuffisantes dans le CSV pour résoudre l'issue dans 60 barres (fins de période).
- **xau_open_no_sweep_fvg manquant** des variants : aucune session de cette semaine n'a produit ce pattern.
- **avg_r=-0.7** : résultat préliminaire sur 5 jours. Pas représentatif — semaine volatile avec fort mouvement haussier atypique.

## Limites

- 5 jours ≪ seuil de 30 jours pour décision perf_status
- 12 trades (dont 4 neutral) ≪ seuil de 20 trades validés
- Prix BID uniquement (pas d'impact significatif pour observation)
- `perf_status` reste `UNMEASURED`

## Prochaine action recommandée

Collecter 30–90 jours pour atteindre le seuil de décision :
```bash
python3 tools/trading_lab/collect_dukascopy_xauusd_m1.py \
  --start 2026-01-06 --end 2026-04-11 \
  --out state/trading_lab_v1/inputs/xauusd_m1_broker_20260106_20260411.csv
```
