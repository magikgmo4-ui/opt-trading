---
doc_id: GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_01_INVENTORY
doc_type: inventory
repo: opt-trading
go_id: GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_01
status: active
source_kind: canonical
updated_at: 2026-05-24
---

# INVENTORY — surfaces Google Sheets / CSV / table-like (repo)

## Objectif

Produire l’inventaire initial des surfaces liées à :

- Google Sheets (sync, controlled write, dry-run)
- exports CSV / logs tabulaires
- contrats table-like (registry, dashboards, fixtures)

Sans modifier le code applicatif, sans API live obligatoire, sans secrets.

## Google Sheets — code exécutable

| Surface | Preuve | Notes |
| --- | --- | --- |
| Daily session controlled sync | `scripts/sheets/sync_daily_session.py` | utilise `gspread` + ADC ; dry-run default ; sheet id via env |
| Orchestration E2E (flags sync) | `scripts/e2e/daily_session_journal.py` | expose un flag “sync sheets” dans une exécution e2e |

### Dépendances

| Dépendance | Preuve |
| --- | --- |
| gspread | `requirements.txt` |
| google-auth | `requirements.txt` |

### Variables d’environnement (noms seulement)

| Variable | Surface | Remarque |
| --- | --- | --- |
| `GOOGLE_SHEETS_SYNC_SHEET_ID` | `scripts/sheets/sync_daily_session.py` | identifie le spreadsheet (clé) |
| `GOOGLE_SHEETS_CREDENTIALS` | `docs/chantiers/GO_EXTERNAL_APPS_BRIDGE_CONTRACTS_01/20_BRIDGE_CONTRACTS.md` | contrat doc-only |
| `GOOGLE_SHEETS_SPREADSHEET_ID` | `docs/chantiers/GO_EXTERNAL_APPS_BRIDGE_CONTRACTS_01/20_BRIDGE_CONTRACTS.md` | contrat doc-only |

## Google Sheets — tests

| Surface | Preuve | Notes |
| --- | --- | --- |
| tests sync daily session | `tests/e2e/test_sync_daily_session.py` | couvre dry-run/controlled-write et invariants |

## Google Sheets — documentation / runbooks

| Surface | Preuve | Notes |
| --- | --- | --- |
| setup credentials / ADC | `docs/chantiers/GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_GOOGLE_SHEETS_*` | setup + fallback + controlled write |
| mapping export stratégie | `docs/chantiers/GO_STRATEGY_CANONICAL_FRAMEWORK_PARENT_01/85_GOOGLE_SHEETS_EXPORT_MAPPING.md` | mapping doc-only |
| cadrage schéma global (déjà présent) | `docs/chantiers/GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_01/10_CURRENT_SHEETS_SURFACES.md` | inventaire initial existant |

## CSV / exports tabulaires (hors Google Sheets)

| Surface | Preuve | Notes |
| --- | --- | --- |
| E2E journal écrit CSV | `scripts/e2e/daily_session_journal.py` | produit `data/journal/daily/<run_id>.csv` |
| datasheet writer CSV | `modules/datasheet_writer/app/writer.py` | écrit `data/datasheet/trades_YYYYMMDD.csv` + JSONL |
| exports stratégie (pandas to_csv) | `tools/strategy/**` | exports backtests/optimizations |

## Trous connus (à compléter par le child inventory)

- surfaces “dashboards / exports” hors `tools/strategy/**` à reclasser par produit final
- registres table-like (YAML/JSON) pouvant jouer un rôle équivalent “sheets_registry”
- doublons entre CSV locaux vs futures tabs Sheets

