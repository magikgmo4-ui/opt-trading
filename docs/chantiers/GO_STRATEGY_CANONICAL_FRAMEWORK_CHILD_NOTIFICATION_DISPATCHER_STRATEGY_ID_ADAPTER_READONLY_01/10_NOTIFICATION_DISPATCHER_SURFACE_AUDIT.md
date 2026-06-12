---
go_id: GO_STRATEGY_CANONICAL_FRAMEWORK_CHILD_NOTIFICATION_DISPATCHER_STRATEGY_ID_ADAPTER_READONLY_01
doc_type: audit
---

# 10_NOTIFICATION_DISPATCHER_SURFACE_AUDIT

## Points d'usage de `strategy_id`

| Fichier | Ligne | Usage |
|---------|-------|-------|
| `app/events.py:38` | Template `signal_received` : `Strategy: <code>{strategy_id}</code>` |
| `app/events.py:81` | `format_message()` : `**event.payload` — `strategy_id` doit être dans le payload |
| `app/dispatcher.py:25` | `dispatch()` : reçoit `PipelineEvent`, appelle `format_message()` |

## Flux

```
PipelineEvent.payload.strategy_id
  → dispatch()
    → format_message()
      → template "Strategy: <code>{strategy_id}</code>"
```

## Point d'insertion

Dans `dispatcher.py`, méthode `NotificationDispatcher.dispatch()`, après `event.validate()` et avant `format_message()` :
- `strategy_id` est accessible via `event.payload.get("strategy_id")`.
- Validation warning-only.
- Pas d'impact sur le template, le message ou l'envoi Telegram.

## RISKS

- À qualifier.
