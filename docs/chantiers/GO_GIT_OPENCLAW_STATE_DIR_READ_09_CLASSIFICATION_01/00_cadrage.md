---
doc_id: GO_GIT_OPENCLAW_STATE_DIR_READ_09_CLASSIFICATION_01
doc_type: chantier
repo: opt-trading
project: opt-trading
go_id: GO_GIT_OPENCLAW_STATE_DIR_READ_09_CLASSIFICATION_01
status: open
lifecycle_stage: classification
updated_at: 2026-04-22
topic_keys:
  - git
  - classification
  - openclaw
  - drop-remote
  - absorbed
surface: docs
source_kind: canonical
links:
  - docs/index/BRANCH_STATE.md
  - docs/governance/GIT_BRANCH_HOUSEKEEPING_WORKFLOW_01.md
  - modules/menu_openclaw/docs/GO_OPENCLAW_STATE_DIR_READ_09.md
  - modules/menu_openclaw/docs/GO_OPENCLAW_INFRA_BASELINE_01.md
---

# GO_GIT_OPENCLAW_STATE_DIR_READ_09_CLASSIFICATION_01 - 00_cadrage

## 1_MASTER_TARGET

Reclassifier `origin/doc/GO_OPENCLAW_STATE_DIR_READ_09` en `DROP_REMOTE_CANDIDATE` et preparer sa sortie du parc remote dans un passage separe.

## 2_INITIAL_PROJECT_DOC

Document de reference initial :
`docs/chantiers/GO_GIT_OPENCLAW_STATE_DIR_READ_09_CLASSIFICATION_01/00_cadrage.md`

## 3_INITIAL_NEED

Verifier le role reel de la branche dans le flux OpenClaw, confirmer son absorption dans `origin/sot/mainline`, puis produire une reclassification strictement doc-only.

## 4_MASTER_PROJECT_PLAN

1. repartir de `docs/index/BRANCH_STATE.md`
2. verifier le delta Git reel de `origin/doc/GO_OPENCLAW_STATE_DIR_READ_09`
3. confirmer le role historique de la branche dans le flux OpenClaw
4. produire la decision doc-only `DROP_REMOTE_CANDIDATE`
5. mettre a jour `docs/index/BRANCH_STATE.md`
6. ne faire aucune suppression remote dans ce passage

## 5_GO_PLAN

Classification doc-only seule, sans :
- suppression Git
- merge
- patch runtime

## RISKS

- À qualifier.
