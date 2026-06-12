---
go_id: GO_STRATEGY_CANONICAL_FRAMEWORK_CHILD_SIGNAL_ROUTER_STRATEGY_ID_ADAPTER_READONLY_01
doc_type: integration
---

# 20_READONLY_ADAPTER_INTEGRATION

## Modification

### `router.py` — fonction `route()`

```python
from modules.strategy.adapter import validate_strategy_id

def route(raw: Mapping[str, Any]) -> NormalizedSignal:
    signal_in = parse_incoming(raw)
    normalized = normalize(signal_in)
    if not validate_strategy_id(normalized.strategy_id):
        log.warning("unknown strategy_id %r", normalized.strategy_id)
    log.info(...)
    return normalized
```

## Principe

- Validation après normalisation : le `strategy_id` est finalisé.
- Warning seulement : pas de `raise`, pas de `sys.exit`, pas de modification du signal.
- Le comportement pipeline est strictement identique avant et après.

## Cas testés

| Scénario | Comportement attendu |
|----------|---------------------|
| `strategy_id` connu (ex: `xau_session_open_v1`) | Silence, aucun warning |
| `strategy_id` inconnu (ex: `breakout_v2`) | Warning log, signal retourné normalement |
| `strategy_id` absent (fallback engine) | Validé via le fallback |

## RISKS

- À qualifier.
