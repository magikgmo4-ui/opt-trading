---
doc_id: GO_OPT_TRADING_DATA_CENTER_CHILD_MARKET_METRICS_WRITER_ENRICH_PRODUCED_AT_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
project: opt-trading
module: derivatives_collector, data_center
go_id: GO_OPT_TRADING_DATA_CENTER_CHILD_MARKET_METRICS_WRITER_ENRICH_PRODUCED_AT_01
parent_go_id: GO_OPT_TRADING_DATA_CENTER_PARENT_OPEN_01
status: open
lifecycle_stage: implementation
created_at: 2026-05-28
updated_at: 2026-05-28
GO_STRUCTURAL_ROLE: GO_CHILD_ATTACHED_TO_PARENT
PF_ID: PF_DATA_CENTER
MASTER_PROJECT_PLAN_ID: MPP_DATA_CENTER_NORMALIZED_REGISTRY
PARENT_GO_ID: GO_OPT_TRADING_DATA_CENTER_PARENT_OPEN_01
BUNDLE_TARGET: MARKET_METRICS_WRITER_DC_ALIGNMENT_V1
topic_keys:
  - opt-trading
  - data_center
  - market_metrics_writer
  - enrich_produced_at
  - schema_validation
links:
  - modules/derivatives_collector/app/market_metrics_writer.py
  - modules/derivatives_collector/app/market_metrics_v1.py
  - modules/data_center/schemas/registry.py
  - modules/data_center/validation/schema_validator.py
  - modules/data_center/storage/manifest_writer.py
---

# GO_OPT_TRADING_DATA_CENTER_CHILD_MARKET_METRICS_WRITER_ENRICH_PRODUCED_AT_01

## Objet

Migrer `market_metrics_writer` vers le Data Center :

1. Aligner le schéma canonique `market_metrics.v1` avec le format réel du payload `MarketMetricsV1`.
2. Ajouter `enrich_produced_at()` pour standardiser le timestamp de production et le marquage `schema`.
3. Valider les payloads via `schema_validator` avant écriture Data Center.
4. Écrire `manifest.json` via `manifest_writer` après write.
5. Préserver la compatibilité des 65 tests existants.

## Contexte

Le `market_metrics_writer` écrit dans `data/data_center/derivatives/` et met à jour le runtime registry, mais :
- Ne valide pas contre le schéma canonique `market_metrics.v1` (utilise sa propre validation `_validate_input_class`)
- N'écrit pas de `manifest.json` Data Center
- Pas de timestamp `produced_at` standardisé

Le schéma `market_metrics.v1` dans le registry est actuellement un schéma générique
(`schema`, `schema_version`, `producer`, `symbol`, `timestamp`, `data`) qui ne correspond
pas au format réel du payload `MarketMetricsV1`.

## Décision architecturale

Le schéma `market_metrics.v1` est mis à jour pour refléter le format canonique du payload
`MarketMetricsV1`. Les tests de validation existants sont mis à jour en conséquence.
C'est un changement borné — le schéma reste un contrat Data Center, mais aligné sur la réalité
du producteur.

## 6_FINAL_TARGET

```text
MarketMetricsV1 payload
  -> enrich_produced_at() (ajoute schema + produced_at)
  -> schema_validator (market_metrics.v1)
  -> write_market_metrics_to_data_center() avec manifest_writer
  -> data/data_center/derivatives/<producer_id>/latest.json
  -> data/data_center/derivatives/<producer_id>/manifest.json
  -> data/data_center/views/market_metrics/latest.json
  -> data/data_center/_registry/producers.json updated
```

## BUNDLE_TARGET — MARKET_METRICS_WRITER_DC_ALIGNMENT_V1

- [ ] `modules/data_center/schemas/registry.py` — `market_metrics.v1` aligné sur MarketMetricsV1
- [ ] `modules/derivatives_collector/app/market_metrics_writer.py` — `enrich_produced_at()` + validation + manifest
- [ ] `tests/data_center/test_schema_validator.py` — payload tests mis à jour
- [ ] Nouveaux tests pour enrich_produced_at + validation + manifest
- [ ] 65 tests existants PASS inchangés
