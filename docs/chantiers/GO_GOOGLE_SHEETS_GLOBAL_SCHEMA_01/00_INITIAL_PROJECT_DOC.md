---
doc_id: GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
go_id: GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_01
status: active
lifecycle_stage: cadrage
source_kind: canonical
updated_at: 2026-05-19
links:
  - docs/chantiers/GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_01/10_CURRENT_SHEETS_SURFACES.md
  - docs/chantiers/GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_01/20_GLOBAL_SCHEMA_TARGET.md
  - docs/chantiers/GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_01/30_PROOF_MATRIX_AND_CONSTRAINTS.md
  - docs/chantiers/GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_01/40_GAPS_AND_NEXT_GO.md
  - docs/chantiers/GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_01/90_REPRISE_POINT.md
  - docs/chantiers/GO_STRATEGY_CANONICAL_FRAMEWORK_PARENT_01/85_GOOGLE_SHEETS_EXPORT_MAPPING.md
  - docs/chantiers/GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_DAILY_SESSION_GOOGLE_SHEETS_CONTROLLED_SYNC_01/00_GO_MASTER.md
---

# 00_INITIAL_PROJECT_DOC - Google Sheets global schema

## But

Standardiser la structure Google Sheets comme consumer transverse (journal + perf + registry), avec:

- un schéma stable (tabs + colonnes)
- une politique de write contrôlée (dry-run par défaut, controlled-write explicite)
- une compatibilité avec l’existant (daily session controlled sync)

## Contraintes

- doc-only dans ce GO (pas d’écriture réelle à Sheets)
- pas de secrets dans le repo (sheet_id / credentials hors repo)
- pas de mélange inbound/outbound (Sheets est un consumer, pas une source)

## Livrables

- `10_CURRENT_SHEETS_SURFACES.md` : surfaces existantes + limites
- `20_GLOBAL_SCHEMA_TARGET.md` : tabs + colonnes cibles V1
- `30_PROOF_MATRIX_AND_CONSTRAINTS.md` : invariants et preuves avant toute écriture
- `40_GAPS_AND_NEXT_GO.md` : plan d’implémentation après schéma
- `90_REPRISE_POINT.md` : reprise + next GO bundle
