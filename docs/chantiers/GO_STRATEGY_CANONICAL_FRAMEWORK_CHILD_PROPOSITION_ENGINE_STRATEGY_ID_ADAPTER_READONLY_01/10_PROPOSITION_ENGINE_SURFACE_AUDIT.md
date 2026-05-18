---
go_id: GO_STRATEGY_CANONICAL_FRAMEWORK_CHILD_PROPOSITION_ENGINE_STRATEGY_ID_ADAPTER_READONLY_01
doc_type: audit
---

# 10_PROPOSITION_ENGINE_SURFACE_AUDIT

## Points d'usage de `strategy_id`

| Fichier | Ligne | Usage |
|---------|-------|-------|
| `app/schema.py:13` | `NormalizedSignal.strategy_id: str` — champ requis |
| `app/schema.py:28` | `from_dict()` : `d.get("strategy_id", "")` |
| `app/engine.py:64` | `PropositionEngine.propose()` — reçoit `request.signal.strategy_id` |
| `app/builder_prompt.py:12` | `strategy={signal.strategy_id}` dans le prompt OpenClaw |
| `app/__main__.py:17` | CLI `--strategy-id` (default `"cli"`) |

## Flux

```
NormalizedSignal (de signal_router)
  → PropositionRequest.signal.strategy_id
    → PropositionEngine.propose()
      → compose_prompt() → inclus dans prompt
```

## Point d'insertion

Dans `engine.py`, méthode `PropositionEngine.propose()`, après l'initialisation de `request_id` et avant `query_engines()` :
- Le `strategy_id` est disponible via `request.signal.strategy_id`.
- La validation n'interfère pas avec les appels aux engines ni la construction du prompt.
- Warning log seulement, pas de modification du flux.
