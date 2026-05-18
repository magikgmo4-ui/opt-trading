---
go_id: GO_STRATEGY_CANONICAL_FRAMEWORK_CHILD_MODULES_STRATEGY_PHYSICAL_CONSOLIDATION_01
doc_type: existing_surface_audit
---

# 10_EXISTING_SURFACE_AUDIT

## Surfaces existantes

| Surface | Chemin | Rôle |
|---------|--------|------|
| Registry | `docs/chantiers/GO_STRATEGY_CANONICAL_FRAMEWORK_PARENT_01/95_STRATEGY_REGISTRY.md` | Source de vérité des stratégies |
| Validateur | `tools/strategy/validate_strategy_registry.py` | Validation strategy_id vs registry |
| Engines | `modules/decision_engine/app/strategy_logic.py` | Logique de trading (hors scope) |

## Décision

Créer une couche physique minimale sans déplacer les engines.
