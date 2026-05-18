---
go_id: GO_STRATEGY_CANONICAL_FRAMEWORK_CHILD_COINM_SHORT_REGISTRY_REGULARIZATION_01
doc_type: registry_entry_proposal
---

# 30_REGISTRY_ENTRY

## Entrée proposée dans 95_STRATEGY_REGISTRY.md

### Table registry — ligne #3

| # | strategy_id | strategy_version | setup_type | status | lifecycle | parent_go |
|---|-------------|-----------------|-----------|--------|-----------|-----------|
| 3 | `COINM_SHORT` | `v0.1.0` | `lower_high_structure_ma_break` | open | CANDIDATE | `GO_STRATEGY_CANONICAL_FRAMEWORK_PARENT_01` |

### Section détaillée 3.3_COINM_SHORT

| Champ | Valeur |
|-------|--------|
| `strategy_id` | `COINM_SHORT` |
| `strategy_version` | `v0.1.0` |
| `setup_type` | `lower_high_structure_ma_break` |
| `family` | `trend_following` |
| `direction` | `SHORT` |
| `lifecycle` | `CANDIDATE` |
| `perf_status` | `UNMEASURED` |
| `go_id` | `GO_STRATEGY_CANONICAL_FRAMEWORK_CHILD_COINM_SHORT_REGISTRY_REGULARIZATION_01` |
| `parent_go` | `GO_STRATEGY_CANONICAL_FRAMEWORK_PARENT_01` |
| `docs_path` | `docs/chantiers/GO_STRATEGY_CANONICAL_FRAMEWORK_CHILD_COINM_SHORT_REGISTRY_REGULARIZATION_01/` |
| `runtime_surfaces` | `strategy_logic.py` (engine), `engines/registry.py`, `webhook_server.py`, `paper_guards.py`, `risk_calculator.py`, `bitget_to_tv_runner.py` |
| `priority` | `P0` |
| `created_at` | `2026-05-18` |

### Justification

- Code engine actif et en production (PR #540 confirmé).
- Priorité #1 dans `pick_one_signal()`.
- Présent dans les guards paper test, le registry engine, et la configuration webhook.
- Default engine pour `bitget_to_tv_runner.py`.
