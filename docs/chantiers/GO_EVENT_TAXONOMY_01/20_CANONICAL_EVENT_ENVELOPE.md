---
doc_id: GO_EVENT_TAXONOMY_01_CANONICAL_EVENT_ENVELOPE
doc_type: contract
repo: opt-trading
go_id: GO_EVENT_TAXONOMY_01
status: active
source_kind: canonical
updated_at: 2026-05-19
---

# 20_CANONICAL_EVENT_ENVELOPE - Enveloppe canonique V1

## Objectif

Définir un envelope minimal permettant:

- typage et routing (`event_type`, `family`)
- traçabilité (`event_id`, timestamps, source)
- compatibilité repo (payload peut être dataclass ou dict existant)

## Enveloppe V1 (minimale)

```json
{
  "event_version": 1,
  "event_id": "<uuid>",
  "event_type": "<string>",
  "family": "<string>",
  "produced_at": "<iso8601 utc>",
  "source": {
    "surface": "<string>",
    "producer": "<string>",
    "machine": "<string|null>"
  },
  "refs": {
    "signal_id": "<string|null>",
    "capture_id": "<string|null>",
    "trade_id": "<string|null>"
  },
  "payload": "<dict|dataclass>",
  "meta": {
    "dry_run": true
  }
}
```

## Règles

- `payload` est **opaque** au routing (routing basé sur `event_type`/`family`), mais doit être sérialisable.
- `meta.dry_run=true` est requis pour toute exécution de validation (fixtures / tests).
- `refs.signal_id` est le pivot principal pour la chaîne trading (quand disponible).

## Notes de compatibilité

- `signal_event` Desk Pro V1 (dict) reste un payload valide.
- Les objets dataclasses des workers (`schema.py`) restent payload valides (conversion via `.to_dict()` ou `asdict`).
