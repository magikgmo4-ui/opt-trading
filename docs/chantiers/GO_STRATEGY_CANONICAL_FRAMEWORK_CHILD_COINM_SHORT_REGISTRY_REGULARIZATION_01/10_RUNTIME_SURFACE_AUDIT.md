---
go_id: GO_STRATEGY_CANONICAL_FRAMEWORK_CHILD_COINM_SHORT_REGISTRY_REGULARIZATION_01
doc_type: runtime_surface_audit
---

# 10_RUNTIME_SURFACE_AUDIT

## Références COINM_SHORT dans le codebase

### Modules Python — 19 matches

| # | Fichier | Ligne | Usage |
|---|---------|-------|-------|
| 1 | `modules/decision_engine/app/strategy_logic.py` | 13 | `Engine.COINM_SHORT = auto()` — enum engine |
| 2 | `modules/decision_engine/app/strategy_logic.py` | 79 | CONFIG `BTCUSDT.P:COINM_SHORT` — niveaux entry zone |
| 3 | `modules/decision_engine/app/strategy_logic.py` | 85 | CONFIG `ETHUSDT.P:COINM_SHORT` — niveaux entry zone |
| 4 | `modules/decision_engine/app/strategy_logic.py` | 111 | `key = f"{ms.symbol}:COINM_SHORT"` — lookup |
| 5 | `modules/decision_engine/app/strategy_logic.py` | 125 | `engine=Engine.COINM_SHORT` — signal production |
| 6 | `modules/decision_engine/app/strategy_logic.py` | 198 | `Engine.COINM_SHORT: 1` — priorité #1 |
| 7 | `modules/engines/registry.py` | 57 | `register_engine("COINM_SHORT", _noop_engine)` |
| 8 | `modules/risk_engine/app/risk_calculator.py` | 77 | Docstring référence `COINM_SHORT` |
| 9 | `modules/webhook/paper_guards.py` | 10 | `AGGRESSIVE_ACTIVE_ENGINES = {"COINM_SHORT", "USDTM_LONG"}` |
| 10 | `webhook_server.py` | 89 | `AGGRESSIVE_ENGINES = {"COINM_SHORT", "USDTM_LONG"}` |
| 11 | `webhook_server.py` | 90 | `ALL_ENGINES = {"COINM_SHORT", "USDTM_LONG", "GOLD_CFD_LONG", ...}` |
| 12 | `tools/bitget_to_tv_runner.py` | 49 | `TV_ENGINE` env var default = `"COINM_SHORT"` |
| 13 | `tests/test_signal_event_adapter.py` | 35 | Payload test engine `"COINM_SHORT"` |
| 14 | `tests/test_signal_event_adapter.py` | 59 | Assert v1 engine `"COINM_SHORT"` |
| 15 | `tests/test_paper_test_runtime_guards.py` | 53 | `active_engine="COINM_SHORT"` |
| 16 | `scripts/smoke_tv_engine.py` | 39 | Commentaire `engine valide (COINM_SHORT)` |
| 17 | `scripts/smoke_tv_engine.py` | 40 | Payload test `"engine": "COINM_SHORT"` |
| 18 | `scripts/smoke_tv_engine.py` | 42 | Assert PASS |
| 19 | `scripts/smoke_tv_engine.py` | 45 | Assert FAIL |

### Surfaces runtime classifiées

| Surface | Fichiers clés | Type |
|---------|---------------|------|
| **Engine core** | `strategy_logic.py` | Logique de trading : signaux, priorité, CONFIG |
| **Engine registry** | `engines/registry.py` | Enregistrement engine comme `_noop_engine` |
| **Webhook gateway** | `webhook_server.py` | Validation engine en entrée |
| **Paper guards** | `webhook/paper_guards.py` | Protection paper test |
| **Risk engine** | `risk_engine/app/risk_calculator.py` | Documentation API |
| **CLI tool** | `tools/bitget_to_tv_runner.py` | TV_ENGINE default |
| **Tests** | `tests/`, `scripts/` | Tests et smoke tests |

### Conclusion

COINM_SHORT est actif sur 5 surfaces runtime distinctes (engine, webhook, guards,
risk, tool). Toutes ces références sont légitimes et cohérentes avec un strategy_id
registré. Aucune référence orpheline ou contradictoire identifiée.

## RISKS

- À qualifier.
