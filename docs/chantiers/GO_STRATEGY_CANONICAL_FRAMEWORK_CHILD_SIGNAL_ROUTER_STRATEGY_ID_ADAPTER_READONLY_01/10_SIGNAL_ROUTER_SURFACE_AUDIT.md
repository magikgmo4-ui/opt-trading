---
go_id: GO_STRATEGY_CANONICAL_FRAMEWORK_CHILD_SIGNAL_ROUTER_STRATEGY_ID_ADAPTER_READONLY_01
doc_type: audit
---

# 10_SIGNAL_ROUTER_SURFACE_AUDIT

## Points d'usage de `strategy_id`

| Fichier | Ligne | Usage |
|---------|-------|-------|
| `app/schema.py:21` | `SignalIn.strategy_id: str = ""` — champ optionnel entrant |
| `app/schema.py:33` | `NormalizedSignal.strategy_id: str` — champ requis normalisé |
| `app/schema.py:47` | `to_dict()` inclut `"strategy_id"` |
| `app/router.py:44` | `parse_incoming()` : extraction du raw, fallback sur `engine` |
| `app/router.py:56` | `normalize()` : propagation vers `NormalizedSignal`, fallback sur `engine` |
| `app/router.py:72` | `route()` : orchestration parse → normalize → return |

## Flux

```
Webhook raw → parse_incoming() → SignalIn.strategy_id (optionnel)
                                  ↓ fallback engine si absent
           → normalize() → NormalizedSignal.strategy_id (requis)
                           ↓
           → route() → retourné → proposition_engine / notification_dispatcher
```

## Point d'insertion

Le meilleur point pour la validation read-only est dans `route()`, après `normalize()` :
- Le `strategy_id` est finalisé (fallback déjà appliqué).
- La validation n'interfère pas avec `parse_incoming()` ou `normalize()`.
- Un warning log peut être émis sans changer le retour.

## RISKS

- À qualifier.
