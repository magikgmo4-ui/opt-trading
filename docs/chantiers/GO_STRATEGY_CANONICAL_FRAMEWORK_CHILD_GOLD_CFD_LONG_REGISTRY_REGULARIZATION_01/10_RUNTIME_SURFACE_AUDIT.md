---
go_id: GO_STRATEGY_CANONICAL_FRAMEWORK_CHILD_GOLD_CFD_LONG_REGISTRY_REGULARIZATION_01
doc_type: runtime_surface_audit
---

# 10_RUNTIME_SURFACE_AUDIT

## Références GOLD_CFD_LONG

| # | Fichier | Ligne | Usage |
|---|---------|-------|-------|
| 1 | `modules/decision_engine/app/strategy_logic.py` | 15 | `Engine.GOLD_CFD_LONG = auto()` |
| 2 | `modules/decision_engine/app/strategy_logic.py` | 101 | CONFIG `XAUUSD:GOLD_CFD_LONG` |
| 3 | `modules/decision_engine/app/strategy_logic.py` | 170 | `key = f"{ms.symbol}:GOLD_CFD_LONG"` |
| 4 | `modules/decision_engine/app/strategy_logic.py` | 183 | `engine=Engine.GOLD_CFD_LONG` |
| 5 | `modules/decision_engine/app/strategy_logic.py` | 199 | `Engine.GOLD_CFD_LONG: 2` — priorité #2 |
| 6 | `modules/engines/registry.py` | 59 | `register_engine("GOLD_CFD_LONG", _noop_engine)` |
| 7 | `modules/risk_engine/app/risk_calculator.py` | 77 | Docstring référence |
| 8 | `modules/risk_engine/app/risk_calculator.py` | 104 | Logique conditionnelle `if engine == "GOLD_CFD_LONG"` |
| 9 | `webhook_server.py` | 90 | `ALL_ENGINES` (non agressif) |

### Particularités

- **Non agressif** : absent de `AGGRESSIVE_ENGINES` et `AGGRESSIVE_ACTIVE_ENGINES`.
- **Logique risk dédiée** : seul engine avec une branche conditionnelle dans `risk_calculator.py:104`.
- **1 instrument** : XAUUSD (gold CFD), timeframe invalidation M15.

## RISKS

- À qualifier.
