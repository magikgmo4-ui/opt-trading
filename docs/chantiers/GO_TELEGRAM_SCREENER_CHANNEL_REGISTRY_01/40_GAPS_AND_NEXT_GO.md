---
doc_id: GO_TELEGRAM_SCREENER_CHANNEL_REGISTRY_01_GAPS_AND_NEXT_GO
doc_type: gaps
repo: opt-trading
go_id: GO_TELEGRAM_SCREENER_CHANNEL_REGISTRY_01
status: active
source_kind: canonical
updated_at: 2026-05-19
---

# 40_GAPS_AND_NEXT_GO

## Gaps restants

| Gap | Impact | Next step |
| --- | --- | --- |
| Registry non implémenté | pas de filtre source | ajouter un loader read-only |
| Parsers non définis | pas de conversion message → event | définir fixtures + parse contracts |
| Event envelope non utilisé côté inbound | pas d’intégration taxonomie | wrapper vers `event_type/family` |
| Aucune surface “telegram listener” | pas d’ingestion | décider API (Bot API getUpdates vs client lib) |

## Next GO bundle

```text
GO_DESKPRO_INPUT_EXPANSION_01
```

Raison: Desk Pro est le hub consumer; une fois inbound/outbound cadrés doc-only, l’extension de l’input map et des outputs doit être fixée avant Google Sheets global.
