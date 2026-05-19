---
go_id: GO_STRATEGY_CANONICAL_FRAMEWORK_CHILD_NOTIFICATION_DISPATCHER_STRATEGY_ID_ADAPTER_READONLY_01
doc_type: integration
---

# 20_READONLY_ADAPTER_INTEGRATION

## Modification

### `dispatcher.py` — `NotificationDispatcher.dispatch()`

```python
from modules.strategy.adapter import validate_strategy_id

class NotificationDispatcher:
    def dispatch(self, event: PipelineEvent, dry_run: bool = False) -> dict[str, Any]:
        event.validate()

        sid = event.payload.get("strategy_id", "")
        if sid and not validate_strategy_id(sid):
            log.warning("unknown strategy_id %r", sid)

        message = format_message(event)
        ...
```

## Principe

- Validation après validation d'event, avant formatage du message.
- Ne s'exécute que si `strategy_id` est présent dans le payload.
- Warning seulement : pas de `raise`, pas de modification du message.
- Le comportement d'envoi est strictement identique avant et après.

## Cas testés

| Scénario | Comportement attendu |
|----------|---------------------|
| `strategy_id` connu dans le payload | Silence, message normal |
| `strategy_id` inconnu dans le payload | Warning log, message normal |
| `strategy_id` absent du payload | Pas de validation, message normal |
