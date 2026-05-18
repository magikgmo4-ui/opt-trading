---
go_id: GO_STRATEGY_CANONICAL_FRAMEWORK_CHILD_USDTM_LONG_REGISTRY_REGULARIZATION_01
doc_type: runtime_surface_audit
---

# 10_RUNTIME_SURFACE_AUDIT

## Références USDTM_LONG dans le codebase

### Modules Python — 11 matches

| # | Fichier | Ligne | Usage |
|---|---------|-------|-------|
| 1 | `modules/decision_engine/app/strategy_logic.py` | 14 | `Engine.USDTM_LONG = auto()` |
| 2 | `modules/decision_engine/app/strategy_logic.py` | 93 | CONFIG `BTCUSDT.P:USDTM_LONG` |
| 3 | `modules/decision_engine/app/strategy_logic.py` | 138 | `key = f"{ms.symbol}:USDTM_LONG"` |
| 4 | `modules/decision_engine/app/strategy_logic.py` | 157 | `engine=Engine.USDTM_LONG` |
| 5 | `modules/decision_engine/app/strategy_logic.py` | 200 | `Engine.USDTM_LONG: 3` — priorité #3 |
| 6 | `modules/engines/registry.py` | 58 | `register_engine("USDTM_LONG", _noop_engine)` |
| 7 | `modules/webhook/paper_guards.py` | 10 | `AGGRESSIVE_ACTIVE_ENGINES` |
| 8 | `webhook_server.py` | 89 | `AGGRESSIVE_ENGINES` |
| 9 | `webhook_server.py` | 90 | `ALL_ENGINES` |
| 10 | `tests/test_signal_event_adapter.py` | 19,49 | Payload + assert test |
| 11 | `tests/fixtures/admin_trading_contract_smoke/signal_event_*.json` | 2,3 | Fixtures JSON engine |

### Surfaces runtime classifiées

| Surface | Type |
|---------|------|
| Engine core (`strategy_logic.py`) | Logique trading : signaux, priorité #3, CONFIG BTC |
| Engine registry (`engines/registry.py`) | Enregistrement engine |
| Webhook gateway (`webhook_server.py`) | Validation engine |
| Paper guards (`paper_guards.py`) | Protection paper test |
| Tests + fixtures | Tests unitaires et fixtures contrat |

### Conclusion

11 références Python cohérentes. USDTM_LONG est engine agressif avec logique
de signal complète (RSI, volume, MAs). Priorité #3 après COINM_SHORT et GOLD_CFD_LONG.
