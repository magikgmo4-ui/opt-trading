---
go_id: GO_STRATEGY_CANONICAL_FRAMEWORK_CHILD_STRATEGY_BACKFILL_DISCOVERY_01
parent_go: GO_STRATEGY_CANONICAL_FRAMEWORK_PARENT_01
doc_type: child_chantier_initial
repo: opt-trading
status: open
surface: doc-only
created_at: 2026-05-18
constraints:
  - no_modules_strategy_consolidation
  - no_runtime_trading_change
  - no_automatic_registry_add
  - no_global_index_modification
---

# GO_STRATEGY_CANONICAL_FRAMEWORK_CHILD_STRATEGY_BACKFILL_DISCOVERY_01

## 00_INITIAL_PROJECT_DOC

---

## 1_OBJECTIF

Identifier toutes les stratégies implicites, canoniques ou semi-canoniques
existantes dans le repo, les classer, et produire une matrice de décision
pour savoir lesquelles promouvoir comme `strategy_id` officiels dans la
registry.

Ce GO ne crée pas `modules/strategy/`. Il ne modifie pas la registry.
Il produit un inventaire et des recommandations.

---

## 2_CONTEXTE

Après 3 PRs de gouvernance stratégie :

| PR | Objet | État |
|---|---|---|
| #536 | SMC ICT strategy child + registry | Mergé |
| #538 | xau_session_open_v1 regularization | Mergé |
| #539 | strategy_id registry validation | Mergé |

La registry contient 2 entrées. Mais plusieurs stratégies historiques
existent ailleurs (engines, presets, GOs, concepts docs) sans être
identifiées comme `strategy_id`.

---

## 3_SCOPE

Surfaces auditées :

```text
- modules/decision_engine/   → Engine enum + strategy_logic.py
- modules/engines/registry.py → Engine string registry
- modules/trading_realtime_v1 → Profile, variants
- modules/trading_lab_v1      → Profile, variants
- docs/ot/trading/            → Schemas, specs, profiles
- docs/chantiers/             → GOs adjacents
- scripts/                    → E2E, smoke
- tools/                      → Perf fixtures
- modules/signal_router       → strategy_id usage
- modules/proposition_engine  → strategy_id usage
- modules/notification_dispatcher → strategy_id usage
```

---

## 4_CONTRAINTES

| Contrainte | Statut |
|---|---|
| doc-only | Oui |
| pas de modules/strategy/ | Oui |
| pas d'ajout automatique registry | Oui |
| pas de modification runtime | Oui |
| classification obligatoire | Oui |

---

## 5_VERDICT_ATTENDU

```text
PASS_STRATEGY_BACKFILL_DISCOVERY_DOC_ONLY
```
