---
doc_id: GO_OPT_TRADING_DEEPSEEK_RUNTIME_CONSOLIDATION_IMPL_02_CADRAGE
doc_type: cadrage
repo: opt-trading
project: opt-trading
module: product
go_id: GO_OPT_TRADING_DEEPSEEK_RUNTIME_CONSOLIDATION_IMPL_02
status: final
lifecycle_stage: closeout
parent_go_id: GO_OPT_TRADING_DEEPSEEK_RUNTIME_CONSOLIDATION_PLAN_01
topic_keys:
  - opt-trading
  - deepseek
  - consolidation
surface: product
source_kind: canonical_draft
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_DEEPSEEK_RUNTIME_CONSOLIDATION_IMPL_02/00_CADRAGE.md
point_de_reprise: "Mise a jour READMEs DeepSeek + marqueur legacy."
updated_at: 2026-05-13
links:
  - docs/chantiers/GO_OPT_TRADING_DEEPSEEK_RUNTIME_CONSOLIDATION_IMPL_01/90_CLOSEOUT.md
---

# 00_CADRAGE — DEEPSEEK_IMPL_02

## 1_MASTER_TARGET

Mettre a jour les READMEs DeepSeek pour documenter la migration vers `student/scripts/` et marquer `scripts/student/` comme legacy.

## 2_CHANGEMENTS

```text
modules/deepseek_student/README.md :
  + mention canonical target student/scripts/
  + lien MIGRATION_STATUS.md

modules/deepseek_hub/README.md :
  + mention canonical target student/scripts/

scripts/student/LEGACY.md :
  + marqueur legacy
  + ne pas supprimer, callers encore actifs
```

## RISKS

- À qualifier.
