---
doc_id: GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_CHILD_INVENTORY_01_REMAINING_GAPS_AND_NEXT_GO
doc_type: gaps
repo: opt-trading
go_id: GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_CHILD_INVENTORY_01
status: open
source_kind: canonical
updated_at: 2026-05-25
---

# 30_REMAINING_GAPS_AND_NEXT_GO

## Gaps (après inventaire V1)

| Gap | Impact | Next step |
| --- | --- | --- |
| Nomenclature tabs non unifiée (liste “registry_*” vs “strategy_*”) | risque de drift avant writer transverse | child “canonical tables” tranche noms + purpose |
| Contrats colonnes non figés par tab | producers futurs incompatibles | child “columns contracts” (types, PK, timestamps, refs) |
| Fixtures CSV par tab absentes | impossible de valider sans API | child “fixtures” produit CSV minimal + tests |
| Règles de validation (anti-dup, nulls, formats) absentes | write non contrôlable | child “validation rules” doc-only + tests de cohérence |
| Mapping producers/consumers incomplet (owners) | table orpheline possible | child “producer/consumer map” durcit mapping + statuts |

## Next GO (proposé)

```text
GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_CHILD_CANONICAL_TABLES_01
```

Raison : avant de détailler colonnes/types, il faut figer la liste/nomenclature des tabs canoniques.

