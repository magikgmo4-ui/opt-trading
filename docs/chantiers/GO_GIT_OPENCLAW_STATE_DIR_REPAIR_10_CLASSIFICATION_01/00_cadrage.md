---
doc_id: GO_GIT_OPENCLAW_STATE_DIR_REPAIR_10_CLASSIFICATION_01
doc_type: chantier
repo: opt-trading
project: opt-trading
go_id: GO_GIT_OPENCLAW_STATE_DIR_REPAIR_10_CLASSIFICATION_01
status: open
lifecycle_stage: classification
updated_at: 2026-04-22
topic_keys:
  - git
  - classification
  - keep-active
  - openclaw
  - state-dir-repair
surface: docs
source_kind: canonical
links:
  - docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_RUNTIME_COMPAT_RETIREMENT_01/00_cadrage.md
---

# GO_GIT_OPENCLAW_STATE_DIR_REPAIR_10_CLASSIFICATION_01 — 00_cadrage

## 1_MASTER_TARGET

Classifier `origin/doc/GO_OPENCLAW_STATE_DIR_REPAIR_10` comme branche conservee et l'exclure du flux cleanup.

## 2_INITIAL_PROJECT_DOC

Document de reference initiale :
`docs/chantiers/GO_GIT_OPENCLAW_STATE_DIR_REPAIR_10_CLASSIFICATION_01/00_cadrage.md`

## 3_INITIAL_NEED

Verifier le role reel de la branche dans le flux OpenClaw et produire une classification doc-only.

## 4_MASTER_PROJECT_PLAN

1. Verifier le contenu de la branche
2. Etablir le role dans le flux OpenClaw
3. Produire le cadrage doc-only
4. Produire la decision doc-only avec statut cible : `KEEP_ACTIVE`
5. Exclure la branche du flux cleanup

## 5_GO_PLAN

Classification doc-only seule, sans :
- suppression
- merge
- patch runtime

## RISKS

- À qualifier.
