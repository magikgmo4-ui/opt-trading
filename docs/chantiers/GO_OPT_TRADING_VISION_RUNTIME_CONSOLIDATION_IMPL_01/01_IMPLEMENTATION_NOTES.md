---
doc_id: GO_OPT_TRADING_VISION_RUNTIME_CONSOLIDATION_IMPL_01_IMPLEMENTATION_NOTES
doc_type: implementation_notes
repo: opt-trading
project: opt-trading
module: product
go_id: GO_OPT_TRADING_VISION_RUNTIME_CONSOLIDATION_IMPL_01
status: draft_for_review
lifecycle_stage: child_implementation_notes
parent_go_id: GO_OPT_TRADING_VISION_RUNTIME_CONSOLIDATION_PLAN_01
topic_keys:
  - opt-trading
  - vision
  - implementation
surface: product
source_kind: canonical_draft
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_VISION_RUNTIME_CONSOLIDATION_IMPL_01/01_IMPLEMENTATION_NOTES.md
point_de_reprise: "Tracer les wrappers ajoutes et leur perimetre exact."
updated_at: 2026-05-07
links:
  - docs/chantiers/GO_OPT_TRADING_VISION_RUNTIME_CONSOLIDATION_IMPL_01/00_CADRAGE.md
---

# 01_IMPLEMENTATION_NOTES

## 1_FICHIERS AJOUTES

```text
modules/vision_bot/scripts/vision_runtime_cmd.sh
modules/vision_bot/scripts/vision_runtime_menu.sh
modules/vision_bot/scripts/vision_runtime_sanity.sh
```

## 2_FICHIERS MODIFIES

```text
modules/vision_bot/scripts/install_shortcuts.sh
modules/vision_bot/README.md
modules/bot_vision_step2/README.md
```

## 3_COMPORTEMENT

```text
Le wrapper unifie expose :
- sanity
- paths
- status
- init
- capture-once
- analyze-latest
- send-latest
- prune-old
- tail
- menu

Il ne modifie pas les services existants.
Il ne remplace pas les anciens raccourcis.
```

## RISKS

- À qualifier.
