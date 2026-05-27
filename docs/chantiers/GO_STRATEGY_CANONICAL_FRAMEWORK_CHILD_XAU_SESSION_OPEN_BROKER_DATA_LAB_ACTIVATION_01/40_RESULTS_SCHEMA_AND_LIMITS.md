---
doc_id: GO_STRATEGY_CANONICAL_FRAMEWORK_CHILD_XAU_SESSION_OPEN_BROKER_DATA_LAB_ACTIVATION_01_RESULTS
doc_type: results
go_id: GO_STRATEGY_CANONICAL_FRAMEWORK_CHILD_XAU_SESSION_OPEN_BROKER_DATA_LAB_ACTIVATION_01
measured_at: 2026-05-27
data_source: sample_xauusd_m1_real_like.csv
---

# 40 — Résultats et schéma de sortie

## Run réalisé sur sample_xauusd_m1_real_like.csv

| Métrique | Valeur |
|---|---|
| Sessions processées | 10 (5 gold_open_18h + 5 midnight_00h) |
| Trades écrits | 10 / 10 (`sequence_complete=True` pour toutes) |
| Dates couvertes | 6 dates (2026-04-07 à 2026-04-14) |
| Période | 8 jours calendaires (1 semaine de trading) |

### Répartition des variants

| Variant | Occurrences |
|---|---|
| `xau_open_sweep_fvg` | 3 |
| `xau_open_no_sweep_no_fvg` | 3 |
| `xau_open_no_sweep_fvg` | 2 |
| `xau_open_sweep_no_fvg` | 2 |

Couverture 4/4 variants ✓

### Répartition directionnelle

| Direction | Occurrences |
|---|---|
| `bullish` | 5 (50%) |
| `bearish` | 5 (50%) |

## Schéma des sorties trading_lab_v1

### features_v1.jsonl (par session)
```json
{
  "feature_id": "feat_YYYYMMDD_HHMMSS_<session>",
  "session_name": "gold_open_18h",
  "local_date": "2026-04-07",
  "sequence_complete": true,
  "variant_id": "xau_open_sweep_fvg",
  "first5_direction": "bullish",
  "sweep_detected": true,
  "fvg_detected": true,
  "first5_range_points": 8.5,
  "entry": 3258.0,
  "sl": 3246.5,
  "rr_planned": 2.0
}
```

### trades_v1.jsonl (par session avec sequence_complete)
```json
{
  "trade_id": "trd_market_YYYYMMDD_HHMMSS_<session>",
  "strategy_id": "xau_session_open_v1",
  "variant_id": "xau_open_sweep_fvg",
  "direction": "bullish",
  "entry": 3258.0,
  "sl": 3246.5,
  "rr_planned": 2.0,
  "result": "open",
  "r_realized": null,
  "execution_state": "virtual_open"
}
```

## Limites de validité

1. **Données synthétiques**: `sample_xauusd_m1_real_like.csv` est un sample construits manuellement, non issu d'un broker réel.
2. **Pas d'exits**: tous les trades restent en `result=open` / `execution_state=virtual_open`. `r_realized=null` pour tous.
3. **Win/Loss non calculable**: pas de mécanisme d'exit implémenté dans `trading_lab_v1` actuellement.
4. **RR réalisé non calculable**: même raison.
5. **Drawdown non calculable**: pas de série temporelle PnL.

## Verdict perf_status

```
perf_status: UNMEASURED
Justification: données sample synthétiques, pas d'exits, pas de production réelle.
               Coverage 4/4 variants validée.
               Runbook broker disponible pour activation réelle future.
```

## Ce qui manque pour MEASURED

| Condition | État |
|---|---|
| ≥ 20 trades closés (`result ∈ {win, loss, breakeven}`) | Non — tous `virtual_open` |
| ≥ 30 jours de sessions réelles | Non — sample 8 jours |
| Source broker réelle (Dukascopy, MT4/MT5) | Non — sample synthétique |
| Mécanisme d'exit dans `trading_lab_v1` | Non implémenté |
