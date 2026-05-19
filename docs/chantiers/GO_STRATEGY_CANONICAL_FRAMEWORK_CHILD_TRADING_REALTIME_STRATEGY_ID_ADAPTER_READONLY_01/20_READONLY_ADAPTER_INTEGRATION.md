---
go_id: GO_STRATEGY_CANONICAL_FRAMEWORK_CHILD_TRADING_REALTIME_STRATEGY_ID_ADAPTER_READONLY_01
doc_type: integration
---

# 20_READONLY_ADAPTER_INTEGRATION

## Modifications apportées

### `runtime_loop_v1.py`

```python
import sys
from modules.strategy.adapter import validate_strategy_id

STRATEGY_ID = "xau_session_open_v1"

if not validate_strategy_id(STRATEGY_ID):
    print(
        f"[WARNING] strategy_id {STRATEGY_ID!r} not found in registry",
        file=sys.stderr,
    )
```

### `event_bridge_v1.py`

Même pattern : import + validation read-only après `STRATEGY_ID`.

## Principe

- La validation est déclenchée une fois à l'import du module (pas à chaque run).
- Elle est purement informative : pas de `raise`, pas de `sys.exit`.
- Le comportement trading est strictement identique avant et après.

## Cas testés

| Scénario | Comportement attendu |
|----------|---------------------|
| `xau_session_open_v1` présent dans registry (actuel) | Silence, aucune sortie |
| `xau_session_open_v1` absent du registry (futur) | Warning stderr, runtime continue |
| Import du module | Validation run, runtime unchanged |
