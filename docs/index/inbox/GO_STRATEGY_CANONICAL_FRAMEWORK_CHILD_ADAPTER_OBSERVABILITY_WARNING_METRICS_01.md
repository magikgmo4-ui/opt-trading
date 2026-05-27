---
doc_id: GO_STRATEGY_CANONICAL_FRAMEWORK_CHILD_ADAPTER_OBSERVABILITY_WARNING_METRICS_01_INBOX
doc_type: inbox_entry
go_id: GO_STRATEGY_CANONICAL_FRAMEWORK_CHILD_ADAPTER_OBSERVABILITY_WARNING_METRICS_01
parent_go: GO_STRATEGY_CANONICAL_FRAMEWORK_PARENT_01
pf_id: PF_STRATEGY_FRAMEWORK_REGISTRY
status: DONE
created_at: 2026-05-27
closed_at: 2026-05-27
pr: "#860"
issue: "#579"
---

# GO_STRATEGY_CANONICAL_FRAMEWORK_CHILD_ADAPTER_OBSERVABILITY_WARNING_METRICS_01

**Objectif** : Ajouter une observabilité minimale et canonique des warnings `strategy_id` inconnus dans `modules/strategy/adapter.py`, sans modifier le comportement runtime/trading.

**Résultat** : PASS_ADAPTER_OBSERVABILITY_WARNING_METRICS_01

## Ce qui a été fait

- `modules/strategy/adapter.py` : ajout de `build_unknown_strategy_warning_payload()` et `log_unknown_strategy_id_warning()`, logger dédié `strategy.observability`
- 6 surfaces migrées vers le helper canonique : signal_router, proposition_engine, notification_dispatcher, trading_realtime_v1/event_bridge_v1, trading_realtime_v1/runtime_loop_v1, trading_lab_v1
- `tests/test_strategy_adapter.py` : 15 nouveaux tests smoke
- 3 fichiers `test_strategy_id_adapter_readonly.py` mis à jour vers le format canonique `STRATEGY_ID_UNKNOWN`

## Résultats tests

| Suite | Résultat |
|-------|----------|
| `tests/test_strategy_adapter.py` (23 nouveaux tests) | 23/23 PASS |
| `signal_router/tests/test_strategy_id_adapter_readonly.py` | 7/7 PASS |
| `proposition_engine/tests/test_strategy_id_adapter_readonly.py` | 5/5 PASS |
| `notification_dispatcher/tests/test_strategy_id_adapter_readonly.py` | 7/7 PASS |
| CI `gate/file-scope`, `gate/preflight`, `gate/no-lock-overlap`, `gate/tests` | 4/4 SUCCESS |

## Chantier

`docs/chantiers/GO_STRATEGY_CANONICAL_FRAMEWORK_CHILD_ADAPTER_OBSERVABILITY_WARNING_METRICS_01/`
