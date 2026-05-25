---
doc_id: GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_CHILD_INVENTORY_01_REPO_INVENTORY
doc_type: inventory
repo: opt-trading
go_id: GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_CHILD_INVENTORY_01
status: open
source_kind: canonical
updated_at: 2026-05-25
---

# 10_REPO_INVENTORY — Google Sheets / CSV / table-like

## Google Sheets (code)

| Surface | Type | Read/Write | Preuve | Notes |
| --- | --- | --- | --- | --- |
| Daily session controlled sync | script | write (controlled) | `scripts/sheets/sync_daily_session.py` | `gspread` + ADC ; dry-run default ; `append_row()` vers `sheet1` |
| Orchestrateur daily session (flags) | script | read local + option sync | `scripts/e2e/daily_session_journal.py` | expose un mode de sync Sheets côté run e2e |

### Variables d’environnement (noms seulement)

| Variable | Preuve | Notes |
| --- | --- | --- |
| `GOOGLE_SHEETS_SYNC_SHEET_ID` | `scripts/sheets/sync_daily_session.py` | sheet key/id du spreadsheet |
| `GOOGLE_SHEETS_CREDENTIALS` | `docs/chantiers/GO_EXTERNAL_APPS_BRIDGE_CONTRACTS_01/20_BRIDGE_CONTRACTS.md` | contrat doc-only |
| `GOOGLE_SHEETS_SPREADSHEET_ID` | `docs/chantiers/GO_EXTERNAL_APPS_BRIDGE_CONTRACTS_01/20_BRIDGE_CONTRACTS.md` | contrat doc-only |

### Dépendances

| Dépendance | Preuve |
| --- | --- |
| `gspread` | `requirements.txt` |
| `google-auth` | `requirements.txt` |

## Google Sheets (tests)

| Surface | Preuve | Read/Write |
| --- | --- | --- |
| tests sync daily session | `tests/e2e/test_sync_daily_session.py` | valide dry-run/controlled-write |

## Google Sheets (docs/runbooks)

| Surface | Preuve | Notes |
| --- | --- | --- |
| setup credentials / ADC / retries | `docs/chantiers/GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_GOOGLE_SHEETS_*` | setup + fallback + controlled write |
| mapping export stratégie (doc-only) | `docs/chantiers/GO_STRATEGY_CANONICAL_FRAMEWORK_PARENT_01/85_GOOGLE_SHEETS_EXPORT_MAPPING.md` | propose des tabs stratégie |
| schéma global (parent) | `docs/chantiers/GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_01/*` | canon V1, doc-first |

## CSV (writes/reads)

### Exports applicatifs

| Surface | Type | Read/Write | Preuve | Output |
| --- | --- | --- | --- | --- |
| datasheet writer | module | write | `modules/datasheet_writer/app/writer.py` | `data/datasheet/trades_YYYYMMDD.csv` + JSONL |

### Exports e2e (journaux)

| Surface | Type | Read/Write | Preuve | Output |
| --- | --- | --- | --- | --- |
| daily_session_journal | script | write | `scripts/e2e/daily_session_journal.py` | `data/journal/daily/<run_id>.csv` |

### Tools stratégie (offline research)

| Zone | Read/Write | Preuve | Notes |
| --- | --- | --- | --- |
| `tools/strategy/**` | read + write | `tools/strategy/**` | exports `to_csv()` ; normalisations de market data |

## Table-like registries (YAML/JSON/CSV)

### Registries YAML (gouvernance)

| Registry | Type | Preuve | Rôle |
| --- | --- | --- | --- |
| `registry/modules_registry.yaml` | YAML | `registry/modules_registry.yaml` | table-like registry |
| `registry/wrappers_registry.yaml` | YAML | `registry/wrappers_registry.yaml` | table-like registry |
| `registry/machines_registry.yaml` | YAML | `registry/machines_registry.yaml` | table-like registry |
| `registry/ui_surfaces_registry.yaml` | YAML | `registry/ui_surfaces_registry.yaml` | table-like registry |

### Data Center registries (JSON)

| Registry | Preuve | Notes |
| --- | --- | --- |
| `modules/data_center/registry/consumers.json` | `modules/data_center/registry/consumers.json` | contient un consumer `google_sheets__market_reporting` `not_started` |
| `modules/data_center/registry/producers.json` | `modules/data_center/registry/producers.json` | chemins d’écriture + IDs |

### CSV “PM/docs”

| Surface | Preuve | Notes |
| --- | --- | --- |
| kanban csv | `docs/project_management/kanban/kanban_board.csv` | usage doc-only |

## Mentions absentes (preuves de scan)

```text
- Aucun usage trouvé de googleapiclient.
- Aucune occurrence trouvée de spreadsheetId / worksheet (gspread utilise sheet1).
```

