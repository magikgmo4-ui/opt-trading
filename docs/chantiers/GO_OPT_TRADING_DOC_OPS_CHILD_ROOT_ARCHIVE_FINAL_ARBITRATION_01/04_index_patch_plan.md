---
doc_id: GO_OPT_TRADING_DOC_OPS_CHILD_ROOT_ARCHIVE_FINAL_ARBITRATION_01_INDEX_PATCH
doc_type: chantier_plan
repo: opt-trading
project: opt-trading
module: governance
go_id: GO_OPT_TRADING_DOC_OPS_CHILD_ROOT_ARCHIVE_FINAL_ARBITRATION_01
status: open
lifecycle_stage: plan
topic_keys:
  - opt-trading
  - governance
  - index_patch
  - root
  - archive
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

- `GO_INDEX.md` : retirer `GO_OPT_TRADING_OBSOLETE_RECLASS_ARCHIVE_AUDIT_01` et `GO_OPT_TRADING_ROOT_POLICY_AND_RECLASS_01`
- `GO_CLOSED_INDEX.md` : ajouter les 2 entrees closes et leurs closeouts
- `ACTIVE_STREAMS.md` : retirer les 2 flux actifs
- `NEXT_GO_CANDIDATES.md` : retirer les 2 parents clos et recalculer la cardinalite active
- `REPRISE.md` : retirer les 2 lignes closes et recalculer le perimetre resserre
- `GO_PARENT_THREAD_MAP.md` : passer les 2 GO en `CLOSED`

## Patch exclu

- aucun patch sur `BRANCH_STATE.md`
- aucun patch runtime
- aucun patch `modules/`
- aucun patch `scripts/`

## RISKS

- À qualifier.
