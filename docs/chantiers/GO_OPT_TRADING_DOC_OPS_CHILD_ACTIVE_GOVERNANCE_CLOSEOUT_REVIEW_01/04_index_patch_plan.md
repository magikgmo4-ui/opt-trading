---
doc_id: GO_OPT_TRADING_DOC_OPS_CHILD_ACTIVE_GOVERNANCE_CLOSEOUT_REVIEW_01_INDEX_PATCH
doc_type: chantier_plan
repo: opt-trading
project: opt-trading
module: governance
go_id: GO_OPT_TRADING_DOC_OPS_CHILD_ACTIVE_GOVERNANCE_CLOSEOUT_REVIEW_01
status: open
lifecycle_stage: plan
topic_keys:
  - opt-trading
  - governance
  - index_patch
surface: chantier
source_kind: canonical
reference_canonique_principale: docs/index/GO_INDEX.md
point_de_reprise: "Section Patch retenu"
updated_at: 2026-04-29
links:
  - docs/index/GO_INDEX.md
  - docs/index/GO_CLOSED_INDEX.md
  - docs/index/ACTIVE_STREAMS.md
  - docs/index/NEXT_GO_CANDIDATES.md
  - docs/index/REPRISE.md
  - docs/index/GO_PARENT_THREAD_MAP.md
---

# 04_index_patch_plan

## Patch retenu

- `GO_INDEX.md` : retirer `CONTINUITY_INDEX_REALIGNMENT_01` et `CANON_STRUCTURE_REALIGNMENT_01` du tableau canonique, de la priorisation et des entrees detaillees
- `GO_CLOSED_INDEX.md` : ajouter les deux entrees closes avec leurs closeouts locaux
- `ACTIVE_STREAMS.md` : retirer les deux flux actifs et recalculer la priorite resserree
- `NEXT_GO_CANDIDATES.md` : retirer les deux parents clos et mettre a jour la cardinalite active
- `REPRISE.md` : retirer les deux lignes closes et recalculer le perimetre resserre
- `GO_PARENT_THREAD_MAP.md` : passer les deux GO de `ACTIVE` a `CLOSED`

## Patch exclu

- aucun patch sur `BRANCH_STATE.md`
- aucun patch runtime
- aucun patch naming
- aucune relecture structurelle globale de `GO_PARENT_THREAD_MAP.md`

## RISKS

- À qualifier.
