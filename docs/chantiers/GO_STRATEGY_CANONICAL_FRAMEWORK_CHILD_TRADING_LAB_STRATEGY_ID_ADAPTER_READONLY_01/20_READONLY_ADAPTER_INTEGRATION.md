---
go_id: GO_STRATEGY_CANONICAL_FRAMEWORK_CHILD_TRADING_LAB_STRATEGY_ID_ADAPTER_READONLY_01
doc_type: integration
---

# 20_READONLY_ADAPTER_INTEGRATION

## Integration

Ajout d'une fonction `resolve_strategy_id(profile)` :

- lit `profile["strategy"].get("strategy_id")` ;
- applique le fallback `xau_session_open_v1` si absent ;
- appelle `validate_strategy_id()` ;
- emet un `log.warning()` seulement si inconnu ;
- retourne exactement la meme valeur qu'avant.

`build_market_event()` utilise ensuite cette valeur resolue sans autre changement.

## Invariants gardes

- aucun changement du fallback ;
- aucun changement de payload event/trade ;
- aucun changement des resultats lab ;
- aucun hard-fail.
