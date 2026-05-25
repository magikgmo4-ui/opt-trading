---
doc_id: GO_DESKPRO_INPUT_EXPANSION_01_GAPS_AND_NEXT_GO
doc_type: gaps
repo: opt-trading
go_id: GO_DESKPRO_INPUT_EXPANSION_01
status: active
source_kind: canonical
updated_at: 2026-05-19
---

# 40_GAPS_AND_NEXT_GO

## Gaps

| Gap | Impact | Next step |
| --- | --- | --- |
| input classes non implémentées | pas de sérialisation uniforme | ajouter wrappers read-only (fixtures-first) |
| refs manquantes (`visual_context_ref`, `desk_snapshot_ref`) | jointure faible | producers doivent remplir refs |
| ~~vision_analysis absent~~ | ~~Desk Pro ne peut pas consommer “vision structured”~~ | **FERMÉ** — GO_DESKPRO_INPUT_EXPANSION_CHILD_VISION_ANALYSIS_READONLY_01 |
| ~~market_metrics absent~~ | ~~scoring incomplet~~ | **FERMÉ** — GO_DESKPRO_INPUT_EXPANSION_CHILD_MARKET_METRICS_READONLY_01 |
| telegram_claim absent | inbound non consommable | registry + parsers + envelope |

## Next GO bundle

```text
GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_01
```

Raison: après cadrage Desk Pro (hub), fixer le schéma global Sheets avant toute implémentation d’écriture transverse.
