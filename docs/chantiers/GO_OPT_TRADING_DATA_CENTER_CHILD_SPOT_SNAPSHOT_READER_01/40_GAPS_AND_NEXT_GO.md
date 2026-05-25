---
doc_id: GO_OPT_TRADING_DATA_CENTER_CHILD_SPOT_SNAPSHOT_READER_01_GAPS
doc_type: gaps_and_next_go
go_id: GO_OPT_TRADING_DATA_CENTER_CHILD_SPOT_SNAPSHOT_READER_01
created_at: 2026-05-25
---

# 40_GAPS_AND_NEXT_GO

## Fermé par ce GO

| Gap | Statut |
|-----|--------|
| GAP-P03 : collector_binance_spot n'écrivait pas dans DC | FERMÉ — `spot_snapshot_dc_writer.py` |
| desk_pro__spot_snapshot `not_started` | FERMÉ — reader + consumers.json |

## Encore ouvert (hors scope)

| Gap | Description |
|-----|-------------|
| `collector_binance_spot` ne câble pas encore `spot_snapshot_dc_writer` dans `run.py` | Phase 2 — nécessite modification du collector runtime |
| `refs/timestamps` dans le payload producer | Traité par GO_REFS_TIMESTAMPS_PRODUCER_STANDARD_01 |
| consumers `not_started` restants | strategy_framework, perf_engine, telegram_screener, google_sheets |

## Note sur le câblage runtime collector

Le bridge `write_spot_snapshot_to_data_center()` est créé et testé avec fixture.
Le collector `run_collection()` ne l'appelle pas encore — c'est intentionnel :
modifier `run.py` est risqué (live API) et hors scope de ce GO fixture-first.
L'intégration runtime est une phase 2 dédiée.

## Prochaine étape

```text
PF_DATA_CENTER : GO_OPT_TRADING_DATA_CENTER_CHILD_REFS_TIMESTAMPS_PRODUCER_STANDARD_01
PF_DATA_CENTER : câblage collector_binance_spot runtime (phase 2 dédiée)
```
