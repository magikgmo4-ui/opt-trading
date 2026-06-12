---
doc_id: GO_OPT_TRADING_VISION_RUNTIME_CONSOLIDATION_PLAN_01_CADRAGE
doc_type: cadrage
repo: opt-trading
project: opt-trading
module: product
go_id: GO_OPT_TRADING_VISION_RUNTIME_CONSOLIDATION_PLAN_01
status: draft_for_review
lifecycle_stage: child_cadrage
parent_go_id: GO_OPT_TRADING_CONSOLIDATION_VISION_CLUSTER_01
topic_keys:
  - opt-trading
  - vision
  - runtime
  - consolidation
  - plan
surface: product
source_kind: canonical_draft
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_VISION_RUNTIME_CONSOLIDATION_PLAN_01/00_CADRAGE.md
point_de_reprise: "Planifier la consolidation runtime du cluster VISION sans l'executer."
updated_at: 2026-05-07
links:
  - docs/chantiers/GO_OPT_TRADING_CONSOLIDATION_VISION_CLUSTER_01/90_CLOSEOUT.md
  - docs/status/bot_vision_canonique.md
---

# 00_CADRAGE — VISION_RUNTIME_CONSOLIDATION_PLAN_01

## 1_MASTER_TARGET

Planifier la consolidation runtime du cluster VISION autour de la paire `vision_bot + bot_vision_step2`, sans deplacement ni fusion executes.

## 2_OBJECTIF

```text
Fixer la topologie runtime exacte :
- inbox / processed / outbox
- services et timers
- captures ShareX / headless_capture
- frontieres vision_bot vs bot_vision_step2
- rollback avant tout changement physique
```

## 3_INCLUS / EXCLUS

```text
INCLUS : topologie, dependances, plan de migration, gate de decision, rollback.
EXCLUS : toute modification systemd, sharex, watchdog, code Python, secrets, runtime.
```

## 12_INVARIANTS

```text
- docs only
- 0 runtime
- 0 migration executee
- 0 changement unit files
- 0 changement chemins shared_files
- 0 secret
```

## RISKS

- À qualifier.
