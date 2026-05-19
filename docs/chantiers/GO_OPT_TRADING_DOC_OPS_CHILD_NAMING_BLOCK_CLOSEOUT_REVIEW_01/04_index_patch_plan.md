---
doc_id: GO_OPT_TRADING_DOC_OPS_CHILD_NAMING_BLOCK_CLOSEOUT_REVIEW_01_INDEX_PATCH
doc_type: chantier_note
repo: opt-trading
project: opt-trading
module: naming_normalizer
go_id: GO_OPT_TRADING_DOC_OPS_CHILD_NAMING_BLOCK_CLOSEOUT_REVIEW_01
status: open
lifecycle_stage: plan
topic_keys:
  - opt-trading
  - naming
  - index_patch
surface: chantier
source_kind: canonical
reference_canonique_principale: docs/index/GO_INDEX.md
point_de_reprise: "Section Patch applique"
updated_at: 2026-04-29
links:
  - docs/index/GO_INDEX.md
  - docs/index/GO_CLOSED_INDEX.md
  - docs/index/GO_PARENT_THREAD_MAP.md
  - docs/index/REPRISE.md
---

# 04_index_patch_plan

## Patch applique
- retirer `GO_OPT_TRADING_CHILD_NAMING_NORMALIZER_01` de `GO_INDEX.md`
- ajouter `GO_OPT_TRADING_CHILD_NAMING_NORMALIZER_01` a `GO_CLOSED_INDEX.md`
- passer `GO_OPT_TRADING_CHILD_NAMING_NORMALIZER_01` en `CLOSED` dans `GO_PARENT_THREAD_MAP.md`
- garder `GO_OPT_TRADING_PARENT_NAMING_CANON_01` et `GO_OPT_TRADING_CHILD_NAMING_INVENTORY_01` ouverts
- mettre a jour `REPRISE.md` et `GO_INDEX.md` pour indiquer que le module est livre et que l'inventaire reste le seul gap naming prioritaire

## Patch non applique
- aucun changement sur `ACTIVE_STREAMS.md` et `NEXT_GO_CANDIDATES.md` au-dela d'une verification de coherence, car le prochain geste naming reste l'inventaire
