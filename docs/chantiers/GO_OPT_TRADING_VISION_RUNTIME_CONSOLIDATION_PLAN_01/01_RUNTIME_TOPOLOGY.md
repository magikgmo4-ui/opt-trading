---
doc_id: GO_OPT_TRADING_VISION_RUNTIME_CONSOLIDATION_PLAN_01_RUNTIME_TOPOLOGY
doc_type: runtime_topology
repo: opt-trading
project: opt-trading
module: product
go_id: GO_OPT_TRADING_VISION_RUNTIME_CONSOLIDATION_PLAN_01
status: draft_for_review
lifecycle_stage: child_runtime_topology
parent_go_id: GO_OPT_TRADING_CONSOLIDATION_VISION_CLUSTER_01
topic_keys:
  - opt-trading
  - vision
  - topology
surface: product
source_kind: canonical_draft
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_VISION_RUNTIME_CONSOLIDATION_PLAN_01/01_RUNTIME_TOPOLOGY.md
point_de_reprise: "Cartographier la topologie runtime VISION avant toute migration."
updated_at: 2026-05-07
links:
  - docs/chantiers/GO_OPT_TRADING_VISION_RUNTIME_CONSOLIDATION_PLAN_01/00_CADRAGE.md
---

# 01_RUNTIME_TOPOLOGY

## 1_FLUX CANONIQUE CIBLE

```text
Capture source
  ├── ShareX
  └── headless_capture (optionnel)
        │
        ▼
shared_files/vision_inbox
        │
        ▼
vision_bot
  ├── preprocess / OCR / packing
  ├── shared_files/vision_processed
  └── shared_files/vision_outbox
        │
        ▼
bot_vision_step2
  ├── analyse vision
  ├── summary.json / analysis.* / logs
  ├── desk pro outputs
  └── telegram send / prune timers
```

## 2_ELEMENTS A RECENSER AVANT MIGRATION

```text
- tous les chemins shared_files reels
- tous les services systemd actifs
- tous les timers actifs
- tous les producers de captures
- tous les callers Telegram et Desk Pro
- tous les alias shell utilises par les operateurs
```

## 3_DECISION GATE

```text
Option A : conserver la paire runtime telle quelle
Option B : fusionner vision_bot + bot_vision_step2 dans un futur survivant unique
Option C : garder pair + archiver bot_vision legacy seulement

Le GO ne tranche pas encore sans inventaire des unit files et des callers.
```

## RISKS

- À qualifier.
