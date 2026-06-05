---
doc_id: GO_OPT_TRADING_DOC_OPS_CHILD_CONTINUITY_ALIGNMENT_AFTER_OPEN_WORK_CONTROL_01_NEXT_FLOW_ARBITRATION
doc_type: decision
repo: opt-trading
project: opt-trading
module:
go_id: GO_OPT_TRADING_DOC_OPS_CHILD_CONTINUITY_ALIGNMENT_AFTER_OPEN_WORK_CONTROL_01
status: open
lifecycle_stage: decision
topic_keys:
  - opt-trading
  - doc_ops
  - next_flow
  - arbitration
surface: chantier
source_kind: canonical
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_DOC_OPS_CHILD_CONTINUITY_ALIGNMENT_AFTER_OPEN_WORK_CONTROL_01/01_gap_matrix.md
point_de_reprise: "Decision retenue"
updated_at: 2026-04-29
links:
  - docs/chantiers/GO_OPT_TRADING_DOC_OPS_PARENT_PROJECT_MACHINE_SPLIT_01/02_go_map.md
  - docs/index/NEXT_GO_CANDIDATES.md
  - docs/index/ACTIVE_STREAMS.md
  - docs/index/REPRISE.md
---

# 02_next_flow_arbitration

## Options lues

### Option A

Passer ensuite a `GO_OPT_TRADING_DOC_OPS_CHILD_PRIMARY_RESTART_01`.

### Option B

Basculer d'abord sur un autre flux P0 deja actif.

### Option C

N'ouvrir aucun nouveau GO tant que les index restent incoherents.

## Decision retenue

Option A, apres PASS du present GO.

## Justification repo-first

- le parent `GO_OPT_TRADING_DOC_OPS_PARENT_PROJECT_MACHINE_SPLIT_01` reste `OPEN` et sa sequence canonique dans `02_go_map.md` est : `BRANCH_CLEANUP` -> `OPEN_WORK_CONTROL` -> `PRIMARY_RESTART` -> `PARENT_TARGET_MAP` ;
- `BRANCH_CLEANUP` ne doit pas etre rouvert ;
- `OPEN_WORK_CONTROL` est clos par PR #166 ;
- l'alignement documentaire des branches est merge par PR #177 et verifie sur `sot/mainline` par PR #178 ;
- les ecarts restants etaient uniquement des ecarts de continuite doc-only sur `GO_INDEX`, `NEXT_GO_CANDIDATES`, `ACTIVE_STREAMS` et `REPRISE` ;
- apres patch minimal et verification, aucun blocage repo-first ne justifie de prendre un autre flux P0 a la place de la suite naturelle du parent ;
- `GO_OPT_TRADING_DOC_OPS_CHILD_PARENT_TARGET_MAP_01` reste interdit avant `PRIMARY_RESTART`.

## Next GO primaire retenu

`GO_OPT_TRADING_DOC_OPS_CHILD_PRIMARY_RESTART_01`

## Conditions

- le present GO doit etre clos en PASS ;
- aucun runtime ne doit etre touche ;
- aucune branche ne doit etre supprimee ;
- `BRANCH_STATE.md` doit rester limite a la surface branches ;
- les 5 parents project/machine restent hors scope jusqu'au GO suivant au minimum.

## RISKS

- À qualifier.
