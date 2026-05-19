---
doc_id: GO_OPT_TRADING_DOC_OPS_CHILD_CONTINUITY_ALIGNMENT_AFTER_OPEN_WORK_CONTROL_01_DECISIONS
doc_type: decision_log
repo: opt-trading
project: opt-trading
module:
go_id: GO_OPT_TRADING_DOC_OPS_CHILD_CONTINUITY_ALIGNMENT_AFTER_OPEN_WORK_CONTROL_01
status: open
lifecycle_stage: decision
topic_keys:
  - opt-trading
  - doc_ops
  - decisions
surface: chantier
source_kind: canonical
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_DOC_OPS_CHILD_CONTINUITY_ALIGNMENT_AFTER_OPEN_WORK_CONTROL_01/01_gap_matrix.md
point_de_reprise: "Section Ce qui reste a faire"
updated_at: 2026-04-29
links:
  - docs/chantiers/GO_OPT_TRADING_DOC_OPS_CHILD_CONTINUITY_ALIGNMENT_AFTER_OPEN_WORK_CONTROL_01/00_cadrage.md
  - docs/chantiers/GO_OPT_TRADING_DOC_OPS_CHILD_CONTINUITY_ALIGNMENT_AFTER_OPEN_WORK_CONTROL_01/02_next_flow_arbitration.md
  - docs/index/GO_INDEX.md
  - docs/index/NEXT_GO_CANDIDATES.md
  - docs/index/ACTIVE_STREAMS.md
  - docs/index/REPRISE.md
  - docs/index/BRANCH_STATE.md
---

# 03_decisions

## Ce qui est etabli

- le parent de reference est `GO_OPT_TRADING_DOC_OPS_PARENT_PROJECT_MACHINE_SPLIT_01` ;
- `GO_OPT_TRADING_DOC_OPS_CHILD_OPEN_WORK_CONTROL_01` est clos ;
- PR #166, PR #177 et PR #178 sont presentes sur `sot/mainline` ;
- le present GO est strictement doc-only ;
- `BRANCH_STATE.md` reste la surface canonique des branches seulement ;
- le prochain flux unique du parent devient `GO_OPT_TRADING_DOC_OPS_CHILD_PRIMARY_RESTART_01` une fois ce lot passe en PASS.

## Ce qui reste hypothese

- aucune hypothese de runtime n'est necessaire pour fermer ce GO ;
- aucune hypothese additionnelle sur les branches n'est necessaire tant que `BRANCH_STATE.md` n'est pas repris dans un GO de housekeeping dedie.

## Ce qui est interdit

- rouvrir `GO_OPT_TRADING_DOC_OPS_CHILD_BRANCH_CLEANUP_01` ;
- rouvrir `GO_OPT_TRADING_DOC_OPS_CHILD_OPEN_WORK_CONTROL_01` ;
- supprimer une branche ;
- modifier un runtime ;
- lancer `GO_OPT_TRADING_DOC_OPS_CHILD_PARENT_TARGET_MAP_01` ;
- ouvrir les 5 parents project/machine ;
- pousser quoi que ce soit sans instruction explicite.

## Ce qui reste a faire

- verifier le diff doc-only du present GO ;
- confirmer que `BRANCH_STATE.md` reste inchange ;
- utiliser `90_closeout.md` comme point de reprise exact ;
- lancer ensuite `GO_OPT_TRADING_DOC_OPS_CHILD_PRIMARY_RESTART_01` si aucune autre contradiction repo-first n'apparait.
