---
doc_id: GO_COLLECTORS_BASELINE_INVENTORY_01_CADRAGE
doc_type: cadrage
repo: opt-trading
project: opt-trading
module: product
go_id: GO_COLLECTORS_BASELINE_INVENTORY_01
status: draft_for_review
lifecycle_stage: child_cadrage
parent_go_id: GO_OPT_TRADING_CONSOLIDATION_COLLECTORS_CLUSTER_01
topic_keys:
  - opt-trading
  - collectors
  - baseline
  - inventory
surface: product
source_kind: canonical_draft
reference_canonique_principale: docs/chantiers/GO_COLLECTORS_BASELINE_INVENTORY_01/00_CADRAGE.md
point_de_reprise: "Produire le baseline inventory demande par COLLECTORS_MIGRATION_MAP_01."
updated_at: 2026-05-07
links:
  - docs/COLLECTORS_MIGRATION_MAP_01.md
  - docs/COLLECTORS_FAMILY_DOCTRINE_01.md
  - docs/chantiers/GO_OPT_TRADING_CONSOLIDATION_COLLECTORS_CLUSTER_01/90_CLOSEOUT.md
---

# 00_CADRAGE — GO_COLLECTORS_BASELINE_INVENTORY_01

## 1_MASTER_TARGET

Produire le baseline inventory du cluster COLLECTORS demande par la migration map : wrappers, configs, outputs, duplications runtime, et consumers downstream.

## 2_PERIMETRE

```text
INCLUS :
- inventory current derivatives_collector wrappers
- inventory config files and output artifacts
- inventory duplicated runtime concerns vs collectors_core
- inventory downstream consumers of derivatives outputs

EXCLUS :
- migration runtime
- refactor collectors
- schema unification
- ajout provider #3
```

## 12_INVARIANTS

```text
- docs only
- 0 runtime
- 0 refactor
- 0 secret
- 0 external connection
```
