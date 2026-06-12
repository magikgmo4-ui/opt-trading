---
doc_id: GO_OPT_TRADING_DEEPSEEK_RUNTIME_CONSOLIDATION_IMPL_01_CADRAGE
doc_type: cadrage
repo: opt-trading
project: opt-trading
module: product
go_id: GO_OPT_TRADING_DEEPSEEK_RUNTIME_CONSOLIDATION_IMPL_01
status: final
lifecycle_stage: closeout
parent_go_id: GO_OPT_TRADING_DEEPSEEK_RUNTIME_CONSOLIDATION_PLAN_01
topic_keys:
  - opt-trading
  - deepseek
  - consolidation
  - implementation
surface: product
source_kind: canonical_draft
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_DEEPSEEK_RUNTIME_CONSOLIDATION_IMPL_01/00_CADRAGE.md
point_de_reprise: "Phase 1 audit callers + Phase 2 migration doc. Aucune suppression."
updated_at: 2026-05-13
links:
  - docs/chantiers/GO_OPT_TRADING_DEEPSEEK_RUNTIME_CONSOLIDATION_PLAN_01/90_CLOSEOUT.md
---

# 00_CADRAGE — DEEPSEEK_RUNTIME_CONSOLIDATION_IMPL_01

## 1_MASTER_TARGET

Executer la Phase 1 (audit) et preparer la Phase 2 (migration doc) du plan DeepSeek, sans supprimer `scripts/student/`.

## 2_EXECUTE

```text
Phase 1 — Audit des callers :
- scripts/post_change.sh → cmd-deepseek_response + cmd-deepseek_thinking
- modules/deepseek_hub/ → cmd-deepseek_student, sanity check
- modules/deepseek_student/ → "do not delete scripts/student/"
- modules/repo_hygiene/ → cleanup notes

Phase 2 — Documentation :
- student/scripts/MIGRATION_STATUS.md ajoute
- etat canonique vs legacy documente
- decision : pas de suppression automatique
```

## 3_NON EXECUTE

```text
- aucun retrait de scripts/student/
- aucun deplacement de fichiers
- aucun changement de shortcuts
- aucun appel a post_change
```

## RISKS

- À qualifier.
