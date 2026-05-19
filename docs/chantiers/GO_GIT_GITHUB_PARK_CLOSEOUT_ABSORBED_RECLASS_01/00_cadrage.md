---
doc_id: GO_GIT_GITHUB_PARK_CLOSEOUT_ABSORBED_RECLASS_01
doc_type: chantier
repo: opt-trading
project: opt-trading
go_id: GO_GIT_GITHUB_PARK_CLOSEOUT_ABSORBED_RECLASS_01
status: open
lifecycle_stage: classification
updated_at: 2026-04-22
topic_keys:
  - git
  - branches
  - github-park
  - closeout
  - drop-remote
surface: docs
source_kind: canonical
links:
  - docs/index/BRANCH_STATE.md
  - docs/governance/GIT_BRANCH_HOUSEKEEPING_WORKFLOW_01.md
---

# GO_GIT_GITHUB_PARK_CLOSEOUT_ABSORBED_RECLASS_01 - 00_cadrage

## 1_MASTER_TARGET

Reclassifier en doc-only le sous-lot PASSE 2 GitHub park / closeout absorbe en `DROP_REMOTE_CANDIDATE`, sans suppression Git dans ce passage.

## 2_INITIAL_PROJECT_DOC

Document de reference initial :
`docs/chantiers/GO_GIT_GITHUB_PARK_CLOSEOUT_ABSORBED_RECLASS_01/00_cadrage.md`

## 3_INITIAL_NEED

Repartir de `docs/index/BRANCH_STATE.md`, verifier le delta Git reel, confirmer l'absorption du sous-lot, puis aligner le canon branches avant un futur passage de suppression remote borne.

## 4_MASTER_PROJECT_PLAN

1. relire `docs/index/BRANCH_STATE.md`
2. verifier l'etat Git reel du sous-lot
3. confirmer l'absorption branche par branche
4. produire la reclassification doc-only en `DROP_REMOTE_CANDIDATE`
5. mettre a jour `docs/index/BRANCH_STATE.md`
6. ne faire aucun delete Git dans ce passage

## 5_GO_PLAN

Sous-lot traite :
- `origin/closeout/collectors-lifecycle-compat-01`
- `origin/docs/github-park-audit-expansion-closeout-01`
- `origin/docs/github-park-branch-trunk-cross-audit-01`

Contraintes :
- doc-only uniquement
- aucune suppression remote
- aucune action sur les branches AI team gelees
- aucune action sur les snapshots
