---
doc_id: GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_01_GAPS_AND_NEXT_GO
doc_type: gaps
repo: opt-trading
go_id: GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_01
status: active
source_kind: canonical
updated_at: 2026-05-25
---

# 40_GAPS_AND_NEXT_GO

## Gaps

| Gap | Impact | Next step |
| --- | --- | --- |
| Tabs 2-5 non implémentées | pas d’export transverse | writer dry-run + mapping |
| Aucun registry Sheets central (tabs names) | fragmentation | utiliser `20_GLOBAL_SCHEMA_TARGET.md` comme canon |
| Sheets API dépendances | write impossible sans env | garder controlled-write strict |
| Conflit multi-writers | double write | single writer module (futur) |

## Next GO bundle

```text
GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_CHILD_COLUMNS_CONTRACTS_01
```

Raison: la liste/nomenclature canonique des feuilles (V1) est maintenant figée ; la prochaine étape est de définir les contrats de colonnes et le plan de fixtures CSV/artefacts, en restant doc-only et fixtures-first.
