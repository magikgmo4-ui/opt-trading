---
doc_id: GO_PERF_ENGINE_STRATEGY_SCORE_01_EVIDENCE_PACK_SCHEMA
doc_type: schema
repo: opt-trading
go_id: GO_PERF_ENGINE_STRATEGY_SCORE_01
status: active
source_kind: canonical
updated_at: 2026-05-19
---

# 30_EVIDENCE_PACK_SCHEMA

## Output JSON (V1)

```json
{
  "strategy_id": "SMC_ICT_CHOCH_BOS_RETEST",
  "strategy_version": "0.1.0",
  "as_of": "2026-05-19T12:00:00+00:00",
  "sample_size": 12,
  "observation_days": 4,
  "metrics": {
    "pass_rate": 0.83,
    "win_rate": 0.50,
    "pnl_cumulative": 123.45,
    "expectancy": 10.29,
    "max_drawdown": -54.0
  },
  "promotion_gate": {
    "verdict": "INSUFFICIENT_SAMPLE",
    "reason": "sample_size_below_threshold",
    "thresholds": {
      "min_sample_size": 30,
      "min_observation_days": 14,
      "min_pass_rate": 0.8
    }
  },
  "retirement_gate": {
    "verdict": "KEEP_OBSERVING"
  }
}
```

## Invariants

- aucun secret dans le pack
- pas d’instruction de trade

## Ancrage umbrella

- `MASTER_TARGET` : standardiser l'evidence pack Perf Engine pour le produit final total
- `Kanban bundle` : reste la carte de navigation principale
- `Prochain item Kanban exact` : `GO_STRATEGY_REGISTRY_TELEGRAM_LATENCY_01`
- `Gaps encore ouverts` : consumer registry absent, export Sheets absent, champs avances du parent encore a etendre si necessaire
