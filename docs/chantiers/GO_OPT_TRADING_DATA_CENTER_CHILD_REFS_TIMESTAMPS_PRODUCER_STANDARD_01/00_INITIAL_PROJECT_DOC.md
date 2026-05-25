---
doc_id: GO_OPT_TRADING_DATA_CENTER_CHILD_REFS_TIMESTAMPS_PRODUCER_STANDARD_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
module: data_center
go_id: GO_OPT_TRADING_DATA_CENTER_CHILD_REFS_TIMESTAMPS_PRODUCER_STANDARD_01
parent_go_id: GO_OPT_TRADING_DATA_CENTER_PARENT_OPEN_01
status: open
created_at: 2026-05-25
updated_at: 2026-05-25
GO_STRUCTURAL_ROLE: GO_CHILD_ATTACHED_TO_PARENT
PF_ID: PF_DATA_CENTER
links:
  - modules/data_center/refs_timestamps.py
  - modules/data_center/tests/test_refs_timestamps.py
  - docs/chantiers/GO_OPT_TRADING_DATA_CENTER_CHILD_REFS_TIMESTAMPS_PRODUCER_STANDARD_01/20_REFS_TIMESTAMPS_STANDARD.md
---

# GO_OPT_TRADING_DATA_CENTER_CHILD_REFS_TIMESTAMPS_PRODUCER_STANDARD_01

## Objet

Standardiser les refs/timestamps producers pour que les payloads DC puissent être
reliés proprement entre surfaces (Desk Pro, Perf Engine, Sheets, Telegram).

Ce GO traite le gap transverse `refs/timestamps = TRANSVERSE_DEFERRED_GAP`
identifié dans `GO_DESKPRO_INPUT_EXPANSION_01`.

## Ce que ce GO ne fait PAS

- Ne modifie pas tous les producers d'un coup.
- Ne casse pas les fixtures historiques.
- Ne rend pas refs/timestamps bloquant pour Desk Pro.
- Aucun appel live, Telegram, OCR, trade.
- Ne ferme pas PF_DATA_CENTER ni PF_DESK_PRO.

## BUNDLE_TARGET

- [x] Inventaire des refs/timestamps existants dans chaque payload
- [x] Standard défini : REQUIRED_CORE / OPTIONAL_BY_CONTRACT / LEGACY_ALLOWED
- [x] `modules/data_center/refs_timestamps.py` — helper `now_utc_z()`, `build_refs()`, `enrich_produced_at()`, `validate_iso_utc()`, `is_compatible_legacy()`
- [x] 23 tests helper — **110 PASS** total DC suite
- [x] Compatibilité legacy documentée — aucune fixture cassée
- [x] Producers ciblés phase 2 documentés
