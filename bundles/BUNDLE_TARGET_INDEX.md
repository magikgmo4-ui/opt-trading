---
doc_id: OPT_TRADING_BUNDLE_TARGET_INDEX
doc_type: bundle_target_index
repo: opt-trading
project: opt-trading
module: bundles
status: draft
lifecycle_stage: bundle_target_tracking
surface: bundles
source_kind: operational_index
updated_at: 2026-05-21
topic_keys:
  - opt-trading
  - bundles
  - target
  - master_target
  - patch_transport
reference_canonique_principale: docs/governance/BUNDLE_TARGET_AND_MASTER_TARGET_METHOD_01.md
point_de_reprise: "Tableau bundle targets"
links:
  - docs/governance/BUNDLE_TARGET_AND_MASTER_TARGET_METHOD_01.md
  - bundles/GO_OPT_TRADING_BUNDLES_CHILD_IDE_DEPORTABLE_PACK_01/TARGETS.md
---

# BUNDLE_TARGET_INDEX

## Objet

Index léger des bundles et de leurs targets.

Cet index ne remplace pas `GO_INDEX.md`, `ACTIVE_STREAMS.md`, `NEXT_GO_CANDIDATES.md`, `REPRISE.md` ni les dossiers chantier.

Il sert uniquement à suivre :

```text
bundle -> target -> master_target -> next bundle / index update candidate
```

## Règles

- Un bundle doit avoir un target.
- Un target doit être rattaché à un master target.
- Un target atteint doit déclencher une évaluation du master target.
- Un master target atteint peut déclencher une proposition de batch d'index globaux.
- Un master target non atteint doit produire un prochain target/bundle candidat.

## Tableau bundle targets

| bundle_go_id | target_id | target_status | master_target_id | master_target_status | next_bundle_candidate | global_index_update_candidate | refs |
|---|---|---|---|---|---|---|---|
| `GO_OPT_TRADING_BUNDLES_CHILD_IDE_DEPORTABLE_PACK_01` | `TARGET_IDE_DEPORTABLE_PATCH_APPLICATION_MATRIX_01` | `ready_for_ide` | `MASTER_TARGET_SESSION_TO_IDE_PATCH_TRANSPORT_01` | `partially_reached` | `TBD_AFTER_FIRST_IDE_USE` | `false` | `bundles/GO_OPT_TRADING_BUNDLES_CHILD_IDE_DEPORTABLE_PACK_01/TARGETS.md`; `bundles/GO_OPT_TRADING_BUNDLES_CHILD_IDE_DEPORTABLE_PACK_01/bundle_meta/target_card.json` |

## Point de reprise

Après application/merge du bundle `GO_OPT_TRADING_BUNDLES_CHILD_IDE_DEPORTABLE_PACK_01`, relire son `target_card.json` et statuer :

```text
target_reached?
master_target_reached?
next_bundle_candidate?
global_index_update_candidate?
```
