---
doc_id: GO_SIGNAL_CHAIN_E2E_DRY_RUN_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
go_id: GO_SIGNAL_CHAIN_E2E_DRY_RUN_01
status: active
lifecycle_stage: cadrage
source_kind: canonical
updated_at: 2026-05-19
links:
  - docs/chantiers/GO_SIGNAL_CHAIN_E2E_DRY_RUN_01/10_CURRENT_SURFACES.md
  - docs/chantiers/GO_SIGNAL_CHAIN_E2E_DRY_RUN_01/20_E2E_STEPS.md
  - docs/chantiers/GO_SIGNAL_CHAIN_E2E_DRY_RUN_01/30_OUTPUT_SCHEMA.md
  - docs/chantiers/GO_SIGNAL_CHAIN_E2E_DRY_RUN_01/40_GAPS_AND_NEXT_GO.md
  - docs/chantiers/GO_SIGNAL_CHAIN_E2E_DRY_RUN_01/90_REPRISE_POINT.md
---

# 00_INITIAL_PROJECT_DOC - E2E dry-run signal chain

## But

Établir un runner E2E reproductible (fixtures-first) qui produit:

- un report pipeline (steps + timestamps)
- un daily session journal (JSON + CSV)
- une sync Sheets en dry-run (preview + audit log)

## Invariants

- aucun ordre live (PAPER only)
- pas d’écriture Google Sheets automatique (controlled-write explicite uniquement)
- pas de secrets dans les artifacts
