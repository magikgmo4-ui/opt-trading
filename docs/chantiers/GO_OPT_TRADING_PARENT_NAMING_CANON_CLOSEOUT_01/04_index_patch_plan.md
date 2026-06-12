---
doc_id: GO_OPT_TRADING_PARENT_NAMING_CANON_CLOSEOUT_01_INDEX_PATCH
doc_type: chantier
repo: opt-trading
project: opt-trading
module:
go_id: GO_OPT_TRADING_PARENT_NAMING_CANON_CLOSEOUT_01
status: open
lifecycle_stage: patch_plan
topic_keys:
  - opt-trading
  - naming
  - index
surface: chantier
source_kind: canonical
reference_canonique_principale: docs/index/GO_INDEX.md
point_de_reprise: "Section Patch retenu"
updated_at: 2026-04-29
links:
  - docs/index/GO_INDEX.md
  - docs/index/GO_CLOSED_INDEX.md
  - docs/index/GO_PARENT_THREAD_MAP.md
  - docs/index/REPRISE.md
  - docs/index/ACTIVE_STREAMS.md
  - docs/index/NEXT_GO_CANDIDATES.md
---

# 04_index_patch_plan

## Patch retenu

- retirer `GO_OPT_TRADING_PARENT_NAMING_CANON_01` de `docs/index/GO_INDEX.md`
- ajouter l'entree closee dans `docs/index/GO_CLOSED_INDEX.md`
- passer le parent en `CLOSED` dans `docs/index/GO_PARENT_THREAD_MAP.md`
- retirer le parent des surfaces operatoires `REPRISE.md`, `ACTIVE_STREAMS.md` et `NEXT_GO_CANDIDATES.md`

## Patch non retenu

- aucun changement sur `BRANCH_STATE.md`
- aucun changement sur runtime, modules ou scripts
- aucun changement d'ouverture d'un apply batch

## RISKS

- À qualifier.
