---
go_id: GO_STRATEGY_CANONICAL_FRAMEWORK_CHILD_TRADING_REALTIME_STRATEGY_ID_ADAPTER_READONLY_01
doc_type: audit
---

# 10_RUNTIME_SURFACE_AUDIT

## Points d'usage de `STRATEGY_ID` dans trading_realtime_v1

| Fichier | Ligne | Usage |
|---------|-------|-------|
| `app/runtime_loop_v1.py` | 13 | `STRATEGY_ID = "xau_session_open_v1"` — constante module |
| `app/runtime_loop_v1.py` | 93 | `"strategy_id": STRATEGY_ID` — injecté dans l'event dict |
| `app/event_bridge_v1.py` | 11 | `STRATEGY_ID = "xau_session_open_v1"` — constante module |
| `app/event_bridge_v1.py` | 71 | `"strategy_id": STRATEGY_ID` — injecté dans l'event dict |

## Analyse

- Les deux constantes sont des strings littérales, identiques.
- Le strategy_id est utilisé uniquement comme champ de données dans l'event JSON, pas pour du routing ou des décisions trading.
- La validation read-only peut être ajoutée au niveau module, une fois à l'import, sans impacter le runtime loop.

## Stratégie de modification

- Dans chaque fichier, importer `validate_strategy_id` depuis `modules.strategy.adapter`.
- Appeler `validate_strategy_id(STRATEGY_ID)` au niveau module, après la définition de `STRATEGY_ID`.
- Si `False` : émettre un warning vers stderr (pas de hard-fail).
- Si `True` : ne rien faire (silence).
