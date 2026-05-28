---
doc_id: GO_OPT_TRADING_DATA_CENTER_CHILD_BINANCE_SPOT_COLLECTOR_RUNTIME_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
project: opt-trading
module: data_center, collector_binance_spot
go_id: GO_OPT_TRADING_DATA_CENTER_CHILD_BINANCE_SPOT_COLLECTOR_RUNTIME_01
parent_go_id: GO_OPT_TRADING_DATA_CENTER_PARENT_OPEN_01
status: open
lifecycle_stage: implementation
surface: docs/chantiers
source_kind: canonical
created_at: 2026-05-28
updated_at: 2026-05-28
GO_STRUCTURAL_ROLE: GO_CHILD_ATTACHED_TO_PARENT
PF_ID: PF_DATA_CENTER
MASTER_PROJECT_PLAN_ID: MPP_DATA_CENTER_NORMALIZED_REGISTRY
PARENT_GO_ID: GO_OPT_TRADING_DATA_CENTER_PARENT_OPEN_01
BUNDLE_TARGET: BINANCE_SPOT_COLLECTOR_RUNTIME_V1
NEXT_ATTACH_TARGET: null
NEXT_GO: GO_OPT_TRADING_DATA_CENTER_CHILD_MARKET_METRICS_WRITER_ENRICH_PRODUCED_AT_01
topic_keys:
  - opt-trading
  - data_center
  - collector_binance_spot
  - pair_market_snapshot
  - schema_registry
  - producer_runtime
links:
  - modules/data_center/schemas/registry.py
  - modules/data_center/validation/schema_validator.py
  - modules/data_center/storage/manifest_writer.py
  - modules/data_center/spot_snapshot_dc_writer.py
  - modules/collector_binance_spot/src/collector_binance_spot/run.py
  - modules/collector_binance_spot/src/collector_binance_spot/normalize.py
  - docs/chantiers/GO_OPT_TRADING_DATA_CENTER_CHILD_PRODUCER_WRITE_VALIDATION_01/10_PRODUCER_WRITE_INVENTORY.md
---

# GO_OPT_TRADING_DATA_CENTER_CHILD_BINANCE_SPOT_COLLECTOR_RUNTIME_01

## Objet

Brancher le producer `collector_binance_spot` sur le Data Center :

1. Déclarer `pair_market_snapshot.v1` dans le registry canonique des schémas.
2. Valider le payload normalisé via `schema_validator` avant écriture Data Center.
3. Écrire le manifest Data Center via `manifest_writer`.
4. Câbler `run_collection()` pour écrire dans `data/data_center/spot/collector_binance_spot/`.
5. Préserver la compatibilité des tests existants.

## Contexte

GAP-P03 identifié dans `PRODUCER_WRITE_VALIDATION_01` :

> `collector_binance_spot` : Câblage `write_pair_market_snapshot_view()` vers producer path `data/data_center/spot/` non fait.

Le collector produit déjà des payloads normalisés (`pair_market_snapshot`) mais ne les écrit pas dans le Data Center. Il écrit uniquement dans `modules/collector_binance_spot/outputs/`.

## Décision architecturale

Le schema `pair_market_snapshot.v1` est un schema canonique Data Center au même titre que `market_metrics.v1`. Il décrit le format de snapshot spot produit par Binance. Contrairement à `market_metrics.v1` qui est un format par-symbole, `pair_market_snapshot.v1` est un snapshot multi-symboles avec une liste de records.

## 6_FINAL_TARGET

```text
collector_binance_spot
  -> normalize_pair_market_snapshot()
  -> validate via schema_validator (pair_market_snapshot.v1)
  -> write_spot_snapshot_to_data_center() with manifest
  -> data/data_center/spot/collector_binance_spot/latest.json
  -> data/data_center/spot/collector_binance_spot/manifest.json
  -> data/data_center/views/pair_market_snapshot/latest.json
  -> data/data_center/_registry/producers.json updated
```

## 12_INVARIANTS

- Ne pas modifier `run.py` existant au-delà de l'ajout de l'appel DC writer après succès.
- Ne pas casser les tests existants du collector (test_binance_spot_module.py).
- Ne pas casser les tests existants du data_center (tests/data_center/).
- Aucun appel API live dans les tests — fixtures uniquement.
- `update_registry` paramétrable (True/False) pour les tests.
- Ne pas fermer PF_DATA_CENTER.

## BUNDLE_TARGET — BINANCE_SPOT_COLLECTOR_RUNTIME_V1

- [ ] `modules/data_center/schemas/registry.py` — registre `pair_market_snapshot.v1`
- [ ] `modules/data_center/spot_snapshot_dc_writer.py` — validation + manifest + amélioration
- [ ] `modules/collector_binance_spot/src/collector_binance_spot/run.py` — appel DC writer
- [ ] `tests/data_center/test_binance_spot_dc_runtime.py` — 5+ tests dc write + validation + manifest
- [ ] Anciens tests inchangés et PASS
