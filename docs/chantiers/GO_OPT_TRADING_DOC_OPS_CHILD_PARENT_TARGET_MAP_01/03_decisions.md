---
doc_id: GO_OPT_TRADING_DOC_OPS_CHILD_PARENT_TARGET_MAP_01_DECISIONS
doc_type: decision_log
repo: opt-trading
project: opt-trading
module:
go_id: GO_OPT_TRADING_DOC_OPS_CHILD_PARENT_TARGET_MAP_01
status: open
lifecycle_stage: decision
topic_keys:
  - opt-trading
  - parent_target_map
  - decisions
surface: chantier
source_kind: canonical
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_DOC_OPS_CHILD_PARENT_TARGET_MAP_01/02_validation_matrix.md
point_de_reprise: "Section Ce qui reste a faire"
updated_at: 2026-04-29
links:
  - docs/chantiers/GO_OPT_TRADING_DOC_OPS_CHILD_PARENT_TARGET_MAP_01/00_cadrage.md
  - docs/chantiers/GO_OPT_TRADING_DOC_OPS_CHILD_PARENT_TARGET_MAP_01/01_parent_target_map.md
  - docs/chantiers/GO_OPT_TRADING_DOC_OPS_CHILD_PARENT_TARGET_MAP_01/02_validation_matrix.md
  - docs/index/GO_INDEX.md
  - docs/index/NEXT_GO_CANDIDATES.md
  - docs/index/ACTIVE_STREAMS.md
  - docs/index/REPRISE.md
---

# 03_decisions

## Ce qui est etabli

- PR #180 est mergee sur `sot/mainline` au commit `6321e7f` ;
- le parent actif reste `GO_OPT_TRADING_DOC_OPS_PARENT_PROJECT_MACHINE_SPLIT_01` ;
- le prochain GO logique devient `GO_OPT_TRADING_DOC_OPS_CHILD_PARENT_TARGET_MAP_01` ;
- une carte cible provisoire a 5 parents est maintenant documentee ;
- aucun parent n'est ouvert dans ce lot ;
- `BRANCH_STATE.md` reste audite et non modifie.

## Ce qui reste hypothese

- la denomination exacte du futur parent `localcms` doit etre arbitree contre l'existant `GO_OPT_TRADING_UI_LOCALCMS_CONSUMER_PARENT_01` ;
- `fantome` reste le candidat le plus fragile et pourrait sortir de l'opening batch si aucune cible durable n'est prouvee ;
- `student` demande encore un arbitrage fin entre lecture machine et lecture famille fonctionnelle.

## Ce qui est interdit

- rouvrir `BRANCH_CLEANUP` ;
- rouvrir `OPEN_WORK_CONTROL` ;
- rouvrir `CONTINUITY_ALIGNMENT_AFTER_OPEN_WORK_CONTROL` ;
- rouvrir `PRIMARY_RESTART` ;
- ouvrir `GO_OPT_TRADING_DOC_OPS_CHILD_PARENT_OPENING_BATCH_01` dans ce lot ;
- ouvrir les 5 parents project/machine ;
- pousser quoi que ce soit sans instruction explicite.

## Ce qui reste a faire

- verifier le diff doc-only final ;
- valider ou corriger la carte cible des 5 parents ;
- utiliser `90_closeout.md` comme point de reprise exact ;
- n'envisager `GO_OPT_TRADING_DOC_OPS_CHILD_PARENT_OPENING_BATCH_01` qu'apres validation explicite de la carte cible.

## RISKS

- À qualifier.
