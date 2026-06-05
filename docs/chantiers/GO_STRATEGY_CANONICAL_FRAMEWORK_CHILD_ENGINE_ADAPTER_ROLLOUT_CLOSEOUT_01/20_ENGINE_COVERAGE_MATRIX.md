---
go_id: GO_STRATEGY_CANONICAL_FRAMEWORK_CHILD_ENGINE_ADAPTER_ROLLOUT_CLOSEOUT_01
doc_type: coverage_matrix
---

# 20_ENGINE_COVERAGE_MATRIX

| Engine | Point d'integration | Mode | Effet comportemental |
|---|---|---|---|
| `trading_realtime_v1` | constantes `STRATEGY_ID` runtime/event bridge | warning-only | aucun |
| `signal_router` | `route()` apres normalisation | warning-only | aucun |
| `proposition_engine` | `PropositionEngine.propose()` | warning-only | aucun |
| `notification_dispatcher` | `NotificationDispatcher.dispatch()` si payload contient `strategy_id` | warning-only | aucun |
| `trading_lab_v1` | resolution YAML/fallback dans `build_market_event()` | warning-only | aucun |

## Couverture finale

```text
trading_realtime_v1 ✅
-> signal_router ✅
-> proposition_engine ✅
-> notification_dispatcher ✅
-> trading_lab_v1 ✅
```

## RISKS

- À qualifier.
