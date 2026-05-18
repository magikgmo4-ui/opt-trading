---
go_id: GO_STRATEGY_CANONICAL_FRAMEWORK_CHILD_MACRO_SECTOR_STAT_STRATEGY_CHECKUP_01
go_type: child
parent_go: GO_STRATEGY_CANONICAL_FRAMEWORK_PARENT_01
repo: opt-trading
status: open
created_at: 2026-05-18
surface: doc-only
---

# GO_STRATEGY_CANONICAL_FRAMEWORK_CHILD_MACRO_SECTOR_STAT_STRATEGY_CHECKUP_01

## 00_INITIAL_PROJECT_DOC

### 1_OBJECTIF

Dernier check doc-only avant consolidation `modules/strategy/`. Auditer et classifier les thèmes macro, sectoriels et statistiques non-runtime : IA, SpaceX/spatial, Brent oil, essence, commodities, watchlist stratégique.

### 2_CONTEXTE

- PR #543 : backfill discovery terminé, 7 entrées registry, 0 UNREGISTERED.
- Certains thèmes (IA, SpaceX, Brent, etc.) ne sont pas des stratégies runtime directes.
- Avant `modules/strategy/`, il faut les classifier pour ne pas les confondre avec des `strategy_id`.

### 3_CLASSIFICATION_RULES

| Classification | Sens |
|---|---|
| `RUNTIME_STRATEGY` | Stratégie exécutable par pipeline, a ou aura un `strategy_id` |
| `STRATEGY_CANDIDATE` | Peut devenir `strategy_id` après validation |
| `MACRO_STRATEGY` | Scénario macro structuré, non exécutable directement |
| `SECTOR_THESIS` | Thème sectoriel long terme (IA, spatial) |
| `STATISTICAL_EDGE` | Edge basé sur stats, saisonnalité, probabilités |
| `WATCHLIST_STRATEGY` | Stratégie de surveillance / scoring / dataset |
| `PORTFOLIO_THEME` | Allocation ou panier d'actifs thématique |
| `NOT_STRATEGY` | Simple contexte, idée non opérable, infra |

### 4_SCOPE

Audit doc-only. Aucune modification registry, aucun changement runtime.
