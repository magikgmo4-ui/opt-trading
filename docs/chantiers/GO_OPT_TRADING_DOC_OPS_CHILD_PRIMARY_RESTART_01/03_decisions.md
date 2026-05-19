---
doc_id: GO_OPT_TRADING_DOC_OPS_CHILD_PRIMARY_RESTART_01_DECISIONS
doc_type: decision_log
repo: opt-trading
project: opt-trading
module:
go_id: GO_OPT_TRADING_DOC_OPS_CHILD_PRIMARY_RESTART_01
status: open
lifecycle_stage: decision
topic_keys:
  - opt-trading
  - primary_restart
  - decisions
surface: chantier
source_kind: canonical
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_DOC_OPS_CHILD_PRIMARY_RESTART_01/01_restart_arbitration.md
point_de_reprise: "Section Ce qui reste a faire"
updated_at: 2026-04-29
links:
  - docs/chantiers/GO_OPT_TRADING_DOC_OPS_CHILD_PRIMARY_RESTART_01/00_cadrage.md
  - docs/chantiers/GO_OPT_TRADING_DOC_OPS_CHILD_PRIMARY_RESTART_01/01_restart_arbitration.md
  - docs/chantiers/GO_OPT_TRADING_DOC_OPS_CHILD_PRIMARY_RESTART_01/02_execution_order.md
  - docs/index/GO_INDEX.md
  - docs/index/NEXT_GO_CANDIDATES.md
  - docs/index/ACTIVE_STREAMS.md
  - docs/index/REPRISE.md
---

# 03_decisions

## Ce qui est etabli

- PR #179 est mergee sur `sot/mainline` au commit `fe42d78` ;
- le parent actif reste `GO_OPT_TRADING_DOC_OPS_PARENT_PROJECT_MACHINE_SPLIT_01` ;
- `GO_OPT_TRADING_DOC_OPS_CHILD_PRIMARY_RESTART_01` devient le flux unique retenu pour cette chaine ;
- les autres P0 actifs restent visibles mais non retenus comme restart de cette sequence ;
- `BRANCH_STATE.md` reste audite et non modifie.

## Ce qui reste hypothese

- aucune hypothese runtime n'est necessaire pour ce GO ;
- aucune hypothese de suppression de branche n'est necessaire ;
- la seule condition exogene restante est la validation humaine du delta doc-only.

## Ce qui est interdit

- rouvrir `GO_OPT_TRADING_DOC_OPS_CHILD_BRANCH_CLEANUP_01` ;
- rouvrir `GO_OPT_TRADING_DOC_OPS_CHILD_OPEN_WORK_CONTROL_01` ;
- rouvrir `GO_OPT_TRADING_DOC_OPS_CHILD_CONTINUITY_ALIGNMENT_AFTER_OPEN_WORK_CONTROL_01` ;
- ouvrir `GO_OPT_TRADING_DOC_OPS_CHILD_PARENT_TARGET_MAP_01` dans ce lot ;
- ouvrir `GO_OPT_TRADING_DOC_OPS_CHILD_PARENT_OPENING_BATCH_01` dans ce lot ;
- ouvrir les 5 parents project/machine ;
- pousser quoi que ce soit sans instruction explicite.

## Ce qui reste a faire

- verifier le diff doc-only final du present GO ;
- confirmer que les surfaces de continuite pointent bien vers `PRIMARY_RESTART` ;
- utiliser `90_closeout.md` comme point de reprise exact ;
- n'envisager `GO_OPT_TRADING_DOC_OPS_CHILD_PARENT_TARGET_MAP_01` qu'apres PASS du present lot.
