---
go_id: GO_STRATEGY_CANONICAL_FRAMEWORK_CHILD_PROPOSITION_ENGINE_STRATEGY_ID_ADAPTER_READONLY_01
doc_type: integration
---

# 20_READONLY_ADAPTER_INTEGRATION

## Modification

### `engine.py` — `PropositionEngine.propose()`

```python
from modules.strategy.adapter import validate_strategy_id

class PropositionEngine:
    def propose(self, request: PropositionRequest) -> Proposition:
        if not request.request_id:
            request.request_id = str(uuid.uuid4())

        if not validate_strategy_id(request.signal.strategy_id):
            log.warning("unknown strategy_id %r", request.signal.strategy_id)

        t0 = time.monotonic()
        ...
```

## Principe

- Validation en début de `propose()` : rapide, avant tout travail.
- Warning seulement : pas de `raise`, pas de modification du `PropositionRequest` ou `Proposition`.
- Le comportement trading est strictement identique avant et après.

## Cas testés

| Scénario | Comportement attendu |
|----------|---------------------|
| `strategy_id` connu (ex: `xau_session_open_v1`) | Silence, proposition normale |
| `strategy_id` inconnu (ex: `test_v1`) | Warning log, proposition normale |

## RISKS

- À qualifier.
