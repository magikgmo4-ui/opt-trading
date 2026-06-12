---
doc_id: GO_GIT_PRODUCT_CARDS_SESSION_ABSORBED_RECLASS_01
doc_type: chantier
repo: opt-trading
project: opt-trading
go_id: GO_GIT_PRODUCT_CARDS_SESSION_ABSORBED_RECLASS_01
status: open
lifecycle_stage: classification
updated_at: 2026-04-22
topic_keys:
  - git
  - branches
  - product
  - cards
  - session
  - absorbed
  - drop-remote
surface: docs
source_kind: canonical
links:
  - docs/index/BRANCH_STATE.md
  - docs/governance/GIT_BRANCH_HOUSEKEEPING_WORKFLOW_01.md
---

# GO_GIT_PRODUCT_CARDS_SESSION_ABSORBED_RECLASS_01 - 00_cadrage

## 1_MASTER_TARGET

Reclassifier en doc-only le sous-lot PASSE 5 Product / cards / session absorbe en `DROP_REMOTE_CANDIDATE`, sans suppression Git dans ce passage.

## 2_INITIAL_PROJECT_DOC

Document de reference initial :
`docs/chantiers/GO_GIT_PRODUCT_CARDS_SESSION_ABSORBED_RECLASS_01/00_cadrage.md`

## 3_INITIAL_NEED

Repartir de `docs/index/BRANCH_STATE.md`, verifier le delta Git reel, confirmer l'absorption du sous-lot, puis aligner le canon branches avant un futur passage borne de suppression remote.

## 4_MASTER_PROJECT_PLAN

1. relire `docs/index/BRANCH_STATE.md`
2. verifier l'etat Git reel du sous-lot Product / cards / session
3. confirmer l'absorption branche par branche
4. produire la reclassification doc-only en `DROP_REMOTE_CANDIDATE`
5. mettre a jour `docs/index/BRANCH_STATE.md`
6. ne faire aucun delete Git dans ce passage

## 5_GO_PLAN

Sous-lot traite :
- `origin/feat/product-target-canon`
- `origin/feat/project-card-bot-vision-ingestion-01`
- `origin/feat/project-card-trading-analytics-chain-01`
- `origin/feat/project-cards-canonical-alignment-01`
- `origin/feat/project-cards-gate-alignment-01`
- `origin/feat/project-portfolio-validated-plans-freeze-01`
- `origin/feat/session-documentation-gate`
- `origin/feat/docs-index-chantier-inventory-sync-01`
- `origin/feat/OT_DESKPRO_RELEASE_OPS_DRILL_01`

Contraintes :
- doc-only uniquement
- aucune suppression remote
- aucune action sur les branches AI team gelees
- aucune action sur les snapshots

## RISKS

- À qualifier.
