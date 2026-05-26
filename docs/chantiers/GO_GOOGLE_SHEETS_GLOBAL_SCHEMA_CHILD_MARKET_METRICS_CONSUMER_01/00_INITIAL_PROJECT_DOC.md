---
doc_id: GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_CHILD_MARKET_METRICS_CONSUMER_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
go_id: GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_CHILD_MARKET_METRICS_CONSUMER_01
go_structural_role: GO_CHILD_ATTACHED_TO_PARENT
parent_go_id: GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_01
pf_id: PF_GOOGLE_SHEETS_CONSUMER
status: open
lifecycle_stage: implementation
surface: modules/google_sheets_global_schema
source_kind: canonical
created_at: 2026-05-25
updated_at: 2026-05-25
upstream:
  - PF_DATA_CENTER
links:
  - docs/chantiers/GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_01/CANONICAL_SHEETS.md
  - docs/chantiers/GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_CHILD_API_WRITE_01/
  - modules/data_center/registry/consumers.json
---

# 00_INITIAL_PROJECT_DOC — Google Sheets market_metrics Consumer V1

## Objectif

Créer le premier consumer réel Data Center → Google Sheets pour le tab `market_metrics`.

**Flux :**
```
data/data_center/views/market_metrics/latest.json   (market_metrics.v1)
  -> map_mm_v1_to_rows()
  -> validate R1-R10
  -> SheetsWriter.write_rows("market_metrics", rows)
```

**Aucun appel Google Sheets API réel par défaut.** FakeSheetsClient dans les tests.

## Contexte validé

- **PR #809** : fixtures V1, validator R1-R10, 41 tests PASS.
- **PR #813** : SheetsWriter + FakeSheetsClient + shared validator.
- `data/data_center/views/market_metrics/latest.json` : source canonique `market_metrics.v1`.
- Consumer `desk_pro__market_metrics` : patron de lecture établi (`market_metrics_reader.py`).
- Consumer `consumers.json` : `"fallback": "silent_empty"` pour source absente.

## Ce GO livre

| Fichier | Rôle |
|---|---|
| `modules/google_sheets_global_schema/market_metrics_consumer.py` | Consumer + mapper market_metrics.v1 → Sheets rows |
| `tests/test_google_sheets_market_metrics_consumer.py` | 21 tests consumer (mapping, validation, fake, no-op, dry-run, isolation API) |

## Règles canoniques

- Data Center = source canonique trading. Sheets = consumer/export.
- Source absente = no-op contrôlé (`ok=True, mode="no_source"`), pas crash.
- Validation R1-R10 appliquée avant tout write.
- Aucun appel Google API sans `ALLOW_GOOGLE_SHEETS_API_WRITE=1` + `spreadsheet_id`.
- Aucun secret dans le code, les logs, ou le repo.

## NE PAS FAIRE

- Appeler Google Sheets API par défaut
- Écrire des credentials dans le repo
- Modifier `.env`
- Faire de Sheets une source canonique trading
- Modifier les producers Data Center
- Brancher datasheet_writer ou learning_feeder runtime dans ce GO
