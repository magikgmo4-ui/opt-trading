---
doc_id: GO_OPT_TRADING_DATA_CENTER_CHILD_REFS_TIMESTAMPS_PRODUCER_STANDARD_01_GAPS
doc_type: gaps_and_next_go
go_id: GO_OPT_TRADING_DATA_CENTER_CHILD_REFS_TIMESTAMPS_PRODUCER_STANDARD_01
created_at: 2026-05-25
---

# 40_GAPS_AND_NEXT_GO

## Fermé par ce GO

| Gap | Statut |
|-----|--------|
| `refs/timestamps producers = TRANSVERSE_DEFERRED_GAP` (depuis GO_DESKPRO_INPUT_EXPANSION_01) | **FERMÉ** — standard documenté, helper créé, tests verts |

## Encore ouvert (phase 2)

| Gap | Description |
|-----|-------------|
| Migration `market_metrics_writer.py` → `enrich_produced_at()` | Phase 2 — risque faible |
| Migration `spot_snapshot_dc_writer.py` → `enrich_produced_at()` | Phase 2 |
| Refs structurées dans nouveaux writers | Phase 3 |
| `visual_context_ref` / `desk_snapshot_ref` dans signal_event producers | Phase 3 |

## Invariant maintenu

- Aucune fixture cassée.
- Desk Pro ne bloque jamais sur refs/timestamps.
- Les join_checks restent WARN, jamais FAIL.

## Prochaine étape

```text
PF_DATA_CENTER : câblage collector_binance_spot → spot_snapshot_dc_writer (phase 2)
PF_DATA_CENTER : migration market_metrics_writer → enrich_produced_at (phase 2)
```
