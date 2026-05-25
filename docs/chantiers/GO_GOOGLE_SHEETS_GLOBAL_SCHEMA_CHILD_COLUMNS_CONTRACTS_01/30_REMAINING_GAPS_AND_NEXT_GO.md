---
doc_id: GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_CHILD_COLUMNS_CONTRACTS_01_REMAINING_GAPS_AND_NEXT_GO
doc_type: gaps
repo: opt-trading
go_id: GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_CHILD_COLUMNS_CONTRACTS_01
status: open
source_kind: canonical
updated_at: 2026-05-25
links:
  - docs/chantiers/GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_CHILD_COLUMNS_CONTRACTS_01/10_COLUMNS_CONTRACTS.md
  - docs/chantiers/GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_CHILD_COLUMNS_CONTRACTS_01/20_FIXTURES_PLAN.md
---

# 30_REMAINING_GAPS_AND_NEXT_GO — Columns Contracts (V1)

## Gaps ouverts

| Gap | Impact | Next step |
| --- | --- | --- |
| Fixtures non matérialisées | pas de preuve parse/validate | générer un pack fixtures V1 |
| Alignement `daily_sessions` (writer actuel = sheet1) | drift de nom de tab | décider rename worksheet vs mapping |
| Registry `sheets_registry` non implémenté | pas de versionning tab | définir modèle minimal + fixture |
| Readers/validators absents | pas de validation structurée | créer validators read-only (futur) |

## Next GO (proposé)

```text
GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_CHILD_FIXTURES_PACK_01
```

Raison: une fois les contrats de colonnes figés, la preuve la plus sûre (sans live Sheets) est un pack de fixtures complet (CSV/JSONL) + checks de validation read-only.
