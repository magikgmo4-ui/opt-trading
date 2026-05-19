---
doc_id: GO_TELEGRAM_EVENT_ROUTING_MAP_01_GAPS_AND_NEXT_GO
doc_type: gaps
repo: opt-trading
go_id: GO_TELEGRAM_EVENT_ROUTING_MAP_01
status: active
source_kind: canonical
updated_at: 2026-05-19
---

# 40_GAPS_AND_NEXT_GO

## Gaps

| Gap | Impact | Fix ciblé |
| --- | --- | --- |
| Un seul chat_id pour tout | bruit + perte de lisibilité | alias map + mapping event→alias |
| Pas de résolution alias → env | pas implémentable sans refactor | introduire une couche de config (sans secrets) |
| Pas de topics supportés | scalabilité limitée | optionnel, après validation |
| Pas de lien direct avec l’enveloppe canonique | routing basé sur un enum local | aligner dispatcher sur `family/type` progressivement |

## Next GO (impl)

```text
GO_TELEGRAM_SCREENER_CHANNEL_REGISTRY_01
```

Raison: une fois le routing outbound cadré, le prochain verrou produit est de poser la registry inbound (channels/trust tiers) sans mélange inbound/outbound.
