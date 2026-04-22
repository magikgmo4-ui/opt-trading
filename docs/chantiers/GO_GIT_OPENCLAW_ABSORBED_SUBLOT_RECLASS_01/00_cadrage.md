---
doc_id: GO_GIT_OPENCLAW_ABSORBED_SUBLOT_RECLASS_01
doc_type: chantier
repo: opt-trading
project: opt-trading
go_id: GO_GIT_OPENCLAW_ABSORBED_SUBLOT_RECLASS_01
status: open
lifecycle_stage: classification
updated_at: 2026-04-22
topic_keys:
  - git
  - branches
  - openclaw
  - absorbed
  - drop-remote
surface: docs
source_kind: canonical
links:
  - docs/index/BRANCH_STATE.md
  - docs/governance/GIT_BRANCH_HOUSEKEEPING_WORKFLOW_01.md
---

# GO_GIT_OPENCLAW_ABSORBED_SUBLOT_RECLASS_01 - 00_cadrage

## 1_MASTER_TARGET

Reclassifier en doc-only le sous-lot OpenClaw absorbe restant de la passe 1 en `DROP_REMOTE_CANDIDATE`, sans suppression Git dans ce passage.

## 2_INITIAL_PROJECT_DOC

Document de reference initial :
`docs/chantiers/GO_GIT_OPENCLAW_ABSORBED_SUBLOT_RECLASS_01/00_cadrage.md`

## 3_INITIAL_NEED

Verifier en read-only que le sous-lot reste absorbe dans `origin/sot/mainline`, confirmer l'absence de commit propre, puis aligner le canon branches avant un futur passage de suppression remote borne.

## 4_MASTER_PROJECT_PLAN

1. repartir de `docs/index/BRANCH_STATE.md`
2. auditer le sous-lot OpenClaw absorbe restant
3. confirmer l'absorption branche par branche
4. reclassifier le sous-lot en `DROP_REMOTE_CANDIDATE`
5. mettre a jour `docs/index/BRANCH_STATE.md`
6. ne faire aucune suppression Git dans ce passage

## 5_GO_PLAN

Sous-lot traite :
- `origin/docs/go-openclaw-evidence-01-v1`
- `origin/docs/openclaw-alignment-decision-07`
- `origin/docs/openclaw-alignment-exception-08`
- `origin/docs/openclaw-alignment-read-06`
- `origin/docs/openclaw-policy-runtime-alignment-05`
- `origin/docs/openclaw-state-dir-vigilance-03`
- `origin/go/openclaw-sync-02-doc`

Contraintes :
- doc-only uniquement
- aucune suppression remote
- aucune action sur les branches AI team gelees
- aucune action sur les snapshots `save/*` ou `backup/mimo-b038db9`
