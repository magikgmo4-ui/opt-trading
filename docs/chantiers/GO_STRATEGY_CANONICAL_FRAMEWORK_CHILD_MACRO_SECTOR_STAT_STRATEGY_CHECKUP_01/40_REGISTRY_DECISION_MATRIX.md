---
go_id: GO_STRATEGY_CANONICAL_FRAMEWORK_CHILD_MACRO_SECTOR_STAT_STRATEGY_CHECKUP_01
doc_type: registry_decision_matrix
---

# 40_REGISTRY_DECISION_MATRIX

## Décision pour chaque thème

| Thème | Classification | Registrable ? | strategy_id ? | Stats ? | Prochain GO ? |
|-------|---------------|---------------|---------------|---------|---------------|
| IA / AI sector thesis | `SECTOR_THESIS` | Non | Non | Non | Rester dans market-structure |
| AI_VISION_STRUCTURE_WATCH | `RUNTIME_STRATEGY` | Oui (futur) | Oui | Oui | Child GO si activé |
| SpaceX / spatial | `SECTOR_THESIS` | Non | Non | Non | Rester dans market-structure |
| Brent oil / crude | `NOT_STRATEGY` | Non | Non | Non | Aucun |
| Energy / commodities | `NOT_STRATEGY` | Non | Non | Non | Aucun |
| Watchlist | `WATCHLIST_STRATEGY` | Non (data layer) | Non | Oui (futur) | Scoring si validé |
| Screener Telegram | `NOT_STRATEGY` | Non | Non | Non | Aucun |
| Seasonality / statistical | `NOT_STRATEGY` | Non | Non | Oui | GO dédié si besoin |
| Portfolio / swing theme | `PORTFOLIO_THEME` | Non | Non | Oui | GO dédié si besoin |
| Macro scenario playbook | `MACRO_STRATEGY` | Oui (futur) | Oui (maybe) | Oui | Child GO si besoin |

## Résultat

**0 nouvelles entrées registry.** Aucun thème audité ne justifie un `strategy_id` aujourd'hui.
La registry reste à 7 entrées. `modules/strategy/` peut être ouvert sans risque de
confusion entre stratégies runtime et thèmes non-opérables.
