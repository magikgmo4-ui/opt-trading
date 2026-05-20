---
doc_id: GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_01_INBOX
repo: opt-trading
project: opt-trading
go_id: GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_01
status: open
surface: index_inbox
source_kind: canonical
updated_at: 2026-05-19
topic_keys:
  - google_sheets
  - schema
  - journal
  - perf
  - registry
  - signal_chain
links:
  - docs/chantiers/GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_01/00_INITIAL_PROJECT_DOC.md
  - docs/chantiers/GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_01/10_CURRENT_SHEETS_SURFACES.md
  - docs/chantiers/GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_01/20_GLOBAL_SCHEMA_TARGET.md
  - docs/chantiers/GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_01/30_PROOF_MATRIX_AND_CONSTRAINTS.md
  - docs/chantiers/GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_01/40_GAPS_AND_NEXT_GO.md
  - docs/chantiers/GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_01/90_REPRISE_POINT.md
---

# INBOX - GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_01

## Objet

Définir un schéma Google Sheets global (tabs + colonnes) pour journal/perf/registry, compatible avec les surfaces déjà présentes (daily session sync) et strictement contrôlé (dry-run par défaut).

## Résultat

État établi :

- surfaces Sheets relues et reconfirmees pour `scripts/sheets/sync_daily_session.py`, `tests/e2e/test_sync_daily_session.py`, `scripts/schedule/daily_session.sh` et `85_GOOGLE_SHEETS_EXPORT_MAPPING.md`
- la seule surface write prouvee reste le daily session sync avec `dry-run` par defaut et `--controlled-write` explicite
- validation relancee dans cette passe : `python -m pytest tests\e2e\test_sync_daily_session.py -q` -> `26 passed`
- aucune mutation runtime introduite ; le chantier reste doc-first et schema-first

## Ancrage umbrella

- `MASTER_TARGET` : contribuer au produit final total via Google Sheets comme consumer transverse
- `Tableau Kanban du bundle` : reste la reference principale
- `Prochain item Kanban exact` : `GO_TELEGRAM_LATENCY_BACKTEST_01`
- `Gaps encore ouverts` : writer transverse unique, tabs 2-5 doc-only, audit log transverse et controlled-write borne

## Point de reprise

```text
docs/chantiers/GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_01/20_GLOBAL_SCHEMA_TARGET.md
docs/chantiers/GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_01/30_PROOF_MATRIX_AND_CONSTRAINTS.md
docs/chantiers/GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_01/40_GAPS_AND_NEXT_GO.md
```
