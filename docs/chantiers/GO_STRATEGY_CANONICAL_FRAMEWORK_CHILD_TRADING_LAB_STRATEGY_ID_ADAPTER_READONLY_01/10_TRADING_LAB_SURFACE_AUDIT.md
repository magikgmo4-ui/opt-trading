---
go_id: GO_STRATEGY_CANONICAL_FRAMEWORK_CHILD_TRADING_LAB_STRATEGY_ID_ADAPTER_READONLY_01
doc_type: audit
---

# 10_TRADING_LAB_SURFACE_AUDIT

## Points d'usage

| Fichier | Ligne | Usage |
|---|---:|---|
| `modules/trading_lab_v1/app/trading_lab_v1.py` | 48 | `load_profile()` lit le YAML |
| `modules/trading_lab_v1/app/trading_lab_v1.py` | 103 | `strategy.strategy_id` parse depuis le YAML |
| `modules/trading_lab_v1/app/trading_lab_v1.py` | 396 | `build_market_event()` applique `profile["strategy"].get("strategy_id") or "xau_session_open_v1"` |
| `modules/trading_lab_v1/app/trading_lab_v1.py` | 424 | `build_trade()` propage `event["strategy_id"]` |

## Conclusion

Le point canonique de validation read-only est la resolution du `strategy_id` dans `build_market_event()` :

- si le YAML contient un `strategy_id`, il est valide tel quel ;
- sinon, le fallback `xau_session_open_v1` est utilise ;
- la validation n'a pas a toucher le parseur YAML lui-meme.
