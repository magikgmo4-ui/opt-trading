---
doc_id: GO_OPT_TRADING_DOC_OPS_CHILD_GOVERNANCE_MATRIX_CONSOLIDATION_CLOSEOUT_01_INDEX_PATCH_PLAN
doc_type: chantier_patch_plan
repo: opt-trading
project: opt-trading
module: continuity
go_id: GO_OPT_TRADING_DOC_OPS_CHILD_GOVERNANCE_MATRIX_CONSOLIDATION_CLOSEOUT_01
status: open
lifecycle_stage: plan
topic_keys:
  - opt-trading
  - indexes
  - patch
  - governance
surface: chantier
source_kind: canonical
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_DOC_OPS_CHILD_GOVERNANCE_MATRIX_CONSOLIDATION_CLOSEOUT_01/02_validation_matrix.md
point_de_reprise: "Section Patch minimal"
updated_at: 2026-04-29
links:
  - docs/index/GO_INDEX.md
  - docs/index/GO_CLOSED_INDEX.md
  - docs/index/NEXT_GO_CANDIDATES.md
  - docs/index/ACTIVE_STREAMS.md
  - docs/index/REPRISE.md
  - docs/index/GO_PARENT_THREAD_MAP.md
---

# 04_index_alignment_patch_plan

## Patch minimal

- `docs/index/GO_INDEX.md`
  - retirer `GO_OPT_TRADING_DOC_OPS_PARENT_PROJECT_MACHINE_SPLIT_01`
  - retirer `GO_OPT_TRADING_DOC_OPS_CHILD_PARENT_CONFORMITY_AUDIT_01`
  - retirer `GO_OPT_TRADING_MATRICE_GOUVERNANTE_METADATA_DERIVATION_01`
  - retirer `GO_OPT_TRADING_REGISTRY_SCOPE_REALIGNMENT_01`
  - retirer `GO_OPT_TRADING_TRAE_PACK_TEXTS_REVISION_01`
  - recalculer la priorite operatoire resserree

- `docs/index/GO_CLOSED_INDEX.md`
  - ajouter les cinq GO clos

- `docs/index/ACTIVE_STREAMS.md`
  - retirer `PROJECT_MACHINE_SPLIT`
  - retirer `METADATA_DERIVATION`
  - retirer `REGISTRY_SCOPE_REALIGNMENT`
  - retirer `TRAE_PACK_TEXTS_REVISION`
  - recalculer la priorite active

- `docs/index/NEXT_GO_CANDIDATES.md`
  - retirer les lignes de parents clos
  - recalculer la priorite active

- `docs/index/REPRISE.md`
  - retirer les lignes devenues hors execution courante
  - corriger la cardinalite active

- `docs/index/GO_PARENT_THREAD_MAP.md`
  - passer `PROJECT_MACHINE_SPLIT` en `CLOSED`
  - passer `PARENT_CONFORMITY_AUDIT` en `CLOSED`
  - passer `METADATA_DERIVATION` en `CLOSED`
  - passer `REGISTRY_SCOPE_REALIGNMENT` en `CLOSED`
  - passer `TRAE_PACK_TEXTS_REVISION` en `CLOSED`

## Exclusions

- ne pas modifier `BRANCH_STATE.md`
- ne pas modifier les index pour `GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01`
- ne pas creer de `GO_CLOSED_INDEX.md` supplementaire
