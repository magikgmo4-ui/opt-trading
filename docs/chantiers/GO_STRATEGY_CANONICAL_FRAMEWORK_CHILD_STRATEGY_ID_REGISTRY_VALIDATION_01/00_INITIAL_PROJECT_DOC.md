---
go_id: GO_STRATEGY_CANONICAL_FRAMEWORK_CHILD_STRATEGY_ID_REGISTRY_VALIDATION_01
parent_go: GO_STRATEGY_CANONICAL_FRAMEWORK_PARENT_01
doc_type: child_chantier_initial
repo: opt-trading
status: open
surface: doc-only + validator tool
created_at: 2026-05-18
constraints:
  - no_modules_strategy_consolidation
  - no_runtime_trading_change
  - no_hard_fail_initial_mode
  - no_global_index_modification
---

# GO_STRATEGY_CANONICAL_FRAMEWORK_CHILD_STRATEGY_ID_REGISTRY_VALIDATION_01

## 00_INITIAL_PROJECT_DOC

---

## 1_OBJECTIF

Ajouter une validation `strategy_id` vs `95_STRATEGY_REGISTRY.md` dans les
surfaces pipeline, pour détecter les `strategy_id` inconnus ou non registrés.

La registry est désormais la source canonique après PR #536 + #538.
Aucune validation ne croise encore les `strategy_id` du pipeline avec cette
registry. Ce GO comble ce gap de gouvernance.

---

## 2_SCOPE

### Surfaces auditées

```text
signal_router          → schema.py, router.py, tests
proposition_engine     → schema.py, builder_prompt.py, __main__.py, tests
notification_dispatcher → events.py, tests
trading_realtime_v1    → runtime_loop_v1.py, event_bridge_v1.py
trading_lab_v1         → trading_lab_v1.py, tests
decision_engine        → aucune référence (scope négatif)
tests/e2e              → dry_run_pipeline.py
```

### Livrables

```text
Couche A — docs :
  00_INITIAL_PROJECT_DOC.md
  10_VALIDATION_SURFACE_AUDIT.md
  20_REGISTRY_VALIDATION_RULE.md
  30_IMPLEMENTATION_PLAN.md
  40_GATE_DECISION.md
  90_CLOSEOUT.md

Couche B — code :
  tools/strategy/validate_strategy_registry.py
```

---

## 3_CONTRAINTES

| Contrainte | Statut |
|---|---|
| doc-only + validator tool | Oui |
| pas de création `modules/strategy/` | Oui |
| pas de refactor pipeline | Oui |
| pas de changement logique trading | Oui |
| pas de blocage CI dur initial | Oui (WARNING_ONLY) |
| pas d'index global modifié | Oui |

---

## 4_VERDICT_ATTENDU

```text
PASS_STRATEGY_ID_REGISTRY_VALIDATION_WARNING_ONLY
```

## RISKS

- À qualifier.
