---
doc_id: GO_OPT_TRADING_VISION_RUNTIME_CONSOLIDATION_IMPL_01_CADRAGE
doc_type: cadrage
repo: opt-trading
project: opt-trading
module: product
go_id: GO_OPT_TRADING_VISION_RUNTIME_CONSOLIDATION_IMPL_01
status: draft_for_review
lifecycle_stage: child_cadrage
parent_go_id: GO_OPT_TRADING_VISION_RUNTIME_CONSOLIDATION_PLAN_01
topic_keys:
  - opt-trading
  - vision
  - runtime
  - implementation
surface: product
source_kind: canonical_draft
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_VISION_RUNTIME_CONSOLIDATION_IMPL_01/00_CADRAGE.md
point_de_reprise: "Implementer un point d'entree unifie non cassant pour la paire VISION."
updated_at: 2026-05-07
links:
  - docs/chantiers/GO_OPT_TRADING_VISION_RUNTIME_CONSOLIDATION_PLAN_01/90_CLOSEOUT.md
---

# 00_CADRAGE — VISION_RUNTIME_CONSOLIDATION_IMPL_01

## 1_MASTER_TARGET

Implementer un point d'entree runtime unifie pour la paire `vision_bot + bot_vision_step2`, sans changer les unit files ni les chemins runtime.

## 2_CHOIX D'IMPLEMENTATION

```text
Implementation retenue :
- nouveaux wrappers shell unifies
- nouveaux raccourcis globaux cmd-vision / menu-vision / sanity-vision
- preservation complete des commandes existantes
```
