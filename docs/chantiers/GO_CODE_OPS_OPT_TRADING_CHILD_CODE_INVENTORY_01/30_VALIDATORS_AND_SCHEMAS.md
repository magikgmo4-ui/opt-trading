---
doc_id: GO_CODE_OPS_OPT_TRADING_CHILD_CODE_INVENTORY_01_VALIDATORS_SCHEMAS
doc_type: inventory_table
repo: opt-trading
project: opt-trading
module: code_ops
go_id: GO_CODE_OPS_OPT_TRADING_CHILD_CODE_INVENTORY_01
status: open
lifecycle_stage: inventory_complete
topic_keys: [validators, schemas, contracts, code_inventory, audit_first]
surface: docs/chantiers
source_kind: canonical
updated_at: 2026-05-28
---

# 30_VALIDATORS_AND_SCHEMAS

## Table C — validateurs

| validator_id | path | validates | input | output | blocking | tests | duplicate_suspect |
|---|---|---|---|---|---|---|---|
| V01 | `tools/governance/validate_master_target_continuity.py` | continuité master target | docs/ | pass/fail | non | — | non |
| V02 | `tools/openclaw/validate_policy_json_report_schema.py` | schéma rapport policy JSON | JSON report | pass/fail | oui | `tests/openclaw/test_validate_policy_json_report_schema.py` | non |
| V03 | `tools/openclaw/validate_runtime_security_all.py` | sécurité runtime | config | pass/fail | oui | `tests/openclaw/test_validate_runtime_security_all.py` | non |
| V04 | `tools/openclaw/validate_skill_policy_static.py` | policy skill statique | JSON | pass/fail | oui | `tests/openclaw/test_validate_skill_policy_static.py` | non |
| V05 | `tools/strategy/validate_strategy_registry.py` | registre stratégie | 95_STRATEGY_REGISTRY.md | pass/fail | non | — | non |
| V06 | `modules/governance/openclaw_mcp_policy_validator/__main__.py` | policy MCP | agents.json5 | JSON report | oui | `tests/openclaw/` | non |
| V07 | `modules/auth/webhook_key.py` | clé webhook | header | bool | oui | — | non |
| V08 | `modules/health/checker.py` | health système | services | dict | non | — | non |
| V09 | `scripts/ai/workers/doc_ops_constraint_check.py` | contraintes doc ops | job | pass/fail | oui | `tests/ai/workers/` | non |
| V10 | `scripts/ai/workers/_validate_job.py` | format job AI | JSON | pass/fail | oui | — | non |
| V11 | `scripts/validate_gh_actions_registries.py` | registres GH Actions | YAML | pass/fail | non | — | non |
| V12 | `tools/why_lint_static_validator/why_lint_static_validator.py` | commentaires why | code | rapport | non | — | non |
| V13 | `modules/validation_gate/app/__main__.py` | gate de validation | payload | pass/fail | oui | `modules/validation_gate/tests/test_gate.py` | non |
| V14 | `modules/trae_module_validator/` | module TRAE | unknown | unknown | unknown | unknown | unknown |

## Table D — schémas / contrats

| contract_id | path | format | consumers | producers | validation |
|---|---|---|---|---|---|
| S01 | `schemas/webhook_event_v1.json` | JSON Schema | webhook_server.py, tests | TradingView | jsonschema |
| S02 | `docs/ot/trading/schemas/trading_event_v1.schema.json` | JSON Schema | perf pipeline | trading_lab_v1 | jsonschema |
| S03 | `docs/ot/trading/schemas/trading_trade_v1.schema.json` | JSON Schema | perf pipeline | execution_engine | jsonschema |
| S04 | `modules/execution_engine/config/sample_decisions.json` | JSON sample | tests | decision_engine | manuel |
| S05 | `modules/execution_engine/config/sample_risk.json` | JSON sample | tests | risk_engine | manuel |
| S06 | `config/machine_runtime_map.yml` | YAML | fleet_orchestrator | ops | manuel |
| S07 | `deploy_module_multi_machine/config/hosts_fallback.json` | JSON | deploy_module | ops | manuel |

## Validateurs suspects / anomalies

| validator_id | path | anomalie | recommandation |
|---|---|---|---|
| — | `modules/trae_module_validator/` | rôle non documenté, non tracé dans CLAUDE.md | qualifier et documenter |
| — | `scripts/validate_gh_actions_registries.py` | hors modules/ et hors tools/ | clarifier placement |

## Schémas sans tests de validation automatique

Les schémas suivants n'ont pas de test de validation automatique identifié :

- `docs/ot/trading/schemas/trading_event_v1.schema.json`
- `docs/ot/trading/schemas/trading_trade_v1.schema.json`
- `modules/execution_engine/config/sample_decisions.json`
- `modules/execution_engine/config/sample_risk.json`

## Note sur la surface vision/coinglass

`modules/vision/coinglass/` contient plusieurs tests de validation :

- `test_ai_extraction.py`
- `test_headless_runner.py`
- `test_parser_mock.py`
- `test_staging_validator.py`
- `test_telegram_sender.py`
- `test_telegram_summary.py`
- `test_vision_context_v1.py`

Ces tests valident le pipeline vision coinglass (headless browser).
Le module est opérationnel mais sa connectivité Coinglass est NOT_PROVEN_RUNTIME_ADAPTER
(contrainte permanente documentée dans CLAUDE.md).
