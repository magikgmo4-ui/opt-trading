---
go_id: GO_STRATEGY_CANONICAL_FRAMEWORK_CHILD_MACRO_SECTOR_STAT_STRATEGY_CHECKUP_01
doc_type: macro_sector_inventory
---

# 20_MACRO_SECTOR_STRATEGY_INVENTORY

## Inventaire détaillé

### IA / AI

**Référence principale** : `GO_STOCK_SPACE_AI_MARKET_STRUCTURE_PARENT_01` (thèse sectorielle)
**Rôle dans le repo** : IA comme thème d'investissement sectoriel (NVDA, AMD couche compute) + infrastructure IA du repo (OpenClaw, DeepSeek, strict workers)

**Conclusion** : `SECTOR_THESIS` — l'IA est un thème sectoriel traité dans market-structure, pas une stratégie runtime.

**Exception** : `AI_VISION_STRUCTURE_WATCH` dans le schema canonique (`20_STRATEGY_CANONICAL_SPEC_SCHEMA.md:138`) est listé comme "AI vision only candidate". Sera régularisé si activé.

### SpaceX / spatial

**Référence principale** : `GO_STOCK_SPACE_AI_MARKET_STRUCTURE_PARENT_01/GO_SPACE_X_ECOSYSTEM_MAP_01_session_plan.md`
**Acteurs couverts** : RKLB (proxy SpaceX), ASTS (telecom spatial), LUNR (lunaire/NASA), PL (data satellite), FLY (lanceur spéculatif)
**Rôle** : Thèse multi-actifs spatial + défense + IA

**Conclusion** : `SECTOR_THESIS` — thèse top-down traitée dans market-structure. Aucun code runtime.

### Brent oil / crude / energy

**Référence** : `STRATEGY_CANDIDATE_INVENTORY.md:77` — "Brent macro/squeeze : Introuvable"
**Conclusion** : `NOT_STRATEGY` — confirmé INFIRMED dans PR #540.

### Commodities

**Référence** : Aucune trouvée.
**Conclusion** : `NOT_STRATEGY` — inexistant dans le repo.

### Seasonality / statistical edge

**Référence** : Aucune trouvée.
**Conclusion** : `NOT_STRATEGY` — inexistant.

### Watchlist

**Référence principale** : Parent `watchlist` (dataset ticker-first)
**Rôle** : Couche dataset des tickers publics + scoring futur. Pas de logique de trading.

**Conclusion** : `WATCHLIST_STRATEGY` — utile comme couche data, pas une stratégie runtime.

### Screener (Telegram Botpress)

**Référence** : Botpress adapter / Telegram smoke tests
**Rôle** : Intent read-only pour market scan via Telegram

**Conclusion** : `NOT_STRATEGY` — c'est un intent Botpress, pas une stratégie.

## RISKS

- À qualifier.
