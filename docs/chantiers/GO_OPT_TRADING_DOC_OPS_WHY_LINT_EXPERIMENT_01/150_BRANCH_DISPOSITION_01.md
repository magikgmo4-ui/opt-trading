---
doc_id: GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_BRANCH_DISPOSITION_01
doc_type: chantier_branch_disposition
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_BRANCH_DISPOSITION_01
parent_go_id: GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01
status: draft
lifecycle_stage: post_merge
topic_keys:
  - why_lint
  - branch_disposition
  - reference_merged
surface: docs/chantiers
source_kind: canonical
updated_at: 2026-05-18
links:
  - docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/140_CLOSEOUT.md
  - docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/GO_OPT_TRADING_DOC_OPS_CHILD_WHY_LINT_STATIC_VALIDATOR_SPEC_01.md
---

# 150_BRANCH_DISPOSITION_01

## Objet

Classer la branche `go/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01` apres merge de la PR `#565`.

## Etat etabli

- PR `#565` mergee vers `sot/mainline`.
- Merge commit : `11efec962c896b449b44e0cab64aa529ee8f1e5d`.
- `origin/sot/mainline` contient deja :
  - `8323c506 docs: add WHY lint experiment reprise`
  - `0739857b docs: add WHY lint static validator spec`
- Scope confirme : doc-only, aucun runtime, aucun index global, aucune branche Claude/artifacts rouverte.
- La branche source n'a pas ete supprimee.

## Decision recommandee

`REFERENCE_MERGED`

## Justification

- Le contenu utile du parent WHY lint et du child GO statique est deja publie sur `sot/mainline`.
- La branche peut rester comme reference de trace tant qu'un lot explicite de housekeeping branches n'est pas ouvert.
- Une suppression immediate recreerait un geste de maintenance distinct sans valeur fonctionnelle supplementaire.

## Interdits sur ce lot

- Ne pas supprimer la branche sans GO cleanup explicite.
- Ne pas rouvrir le parent WHY lint comme chantier actif a partir de la seule existence de la branche.
- Ne pas modifier les index globaux dans ce passage.

## Resume point

Si un lot de housekeeping est ouvert plus tard :

1. repartir de cette note de disposition ;
2. verifier de nouveau que `sot/mainline` contient toujours le contenu merge ;
3. decider alors entre conservation reference ou suppression operee.
