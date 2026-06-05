---
doc_id: GO_OPT_TRADING_DOC_OPS_CHILD_GO_PARENT_THREAD_INDEX_PROMOTION_01_DECISIONS
doc_type: decisions
repo: opt-trading
project: opt-trading
module:
go_id: GO_OPT_TRADING_DOC_OPS_CHILD_GO_PARENT_THREAD_INDEX_PROMOTION_01
status: open
lifecycle_stage: audit
topic_keys:
  - opt-trading
  - parent_thread_map
  - index
  - decisions
surface: chantier
source_kind: canonical
reference_canonique_principale: docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
point_de_reprise: "Section Decisions"
updated_at: 2026-04-29
links:
  - docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
  - docs/chantiers/GO_OPT_TRADING_DOC_OPS_CHILD_GO_PARENT_THREAD_INDEX_PROMOTION_01/01_index_promotion_review.md
  - docs/chantiers/GO_OPT_TRADING_DOC_OPS_CHILD_GO_PARENT_THREAD_INDEX_PROMOTION_01/02_index_contract.md
---

# 03_decisions — Decisions

## Decision 1 : CREER GO_PARENT_THREAD_MAP.md

L'audit confirme l'utilite de l'index comme vue derivee legere. Decision : CREER.

## Decision 2 : source_kind = derived

L'index est explicitement declare comme `source_kind: derived`. Il n'est pas une source canonique.

## Decision 3 : reference_canonique_principale = GO_INDEX.md

L'index reference GO_INDEX.md comme source canonique principale. Toute divergence est a resoudre contre GO_INDEX.md.

## Decision 4 : table unique, pas de duplication des Entrees

L'index contient une table unique GO -> parent -> fil -> action. Il ne duplique pas les Entrees detaillees de GO_INDEX.md.

## Decision 5 : pas de modification de GO_INDEX.md

Ce lot ne modifie pas GO_INDEX.md. L'index est un ajout, pas un remplacement.

## Decision 6 : regles de priorite entre index

Les regles de priorite sont documentees dans le contrat (02_index_contract.md). GO_INDEX.md reste souverain.

## RISKS

- À qualifier.
