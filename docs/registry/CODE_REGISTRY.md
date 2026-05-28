---
doc_id: OPT_TRADING_CODE_REGISTRY_V1
doc_type: code_registry
repo: opt-trading
project: opt-trading
module: code_ops
go_id: GO_CODE_OPS_OPT_TRADING_CHILD_CODE_REGISTRY_01
status: open
lifecycle_stage: v1_core_entries
topic_keys:
  - opt-trading
  - code_registry
  - code_ops
  - refactor
  - normalization
surface: docs/registry
source_kind: canonical
schema_version: "0.1.0"
updated_at: 2026-05-28
links:
  - docs/chantiers/GO_CODE_OPS_OPT_TRADING_CHILD_CODE_INVENTORY_01/10_FILE_INVENTORY.md
  - docs/chantiers/GO_CODE_OPS_OPT_TRADING_CHILD_CODE_REGISTRY_01/10_DEDUP_QUALIFICATIONS.md
  - docs/chantiers/GO_CODE_OPS_OPT_TRADING_PARENT_REFACTOR_NORMALIZATION_01/20_CODE_REGISTRY_SPEC.md
---

# CODE_REGISTRY — opt-trading v1

Registre canonique du code `opt-trading`.
Produit par `GO_CODE_OPS_OPT_TRADING_CHILD_CODE_REGISTRY_01` (2026-05-28).
Source : inventaire `GO_CODE_OPS_OPT_TRADING_CHILD_CODE_INVENTORY_01`.

**Règle** : ce registre documente. Il ne supprime pas, ne renomme pas, ne réorganise pas.
La réalité du repo prime sur toute entrée du registre.

---

## Légende

| Champ | Valeurs possibles |
|---|---|
| `role` | runtime / cli / validator / adapter / schema / collector / orchestrator / wrapper / helper / test / unknown |
| `status` | ACTIVE / CANDIDATE / EXPERIMENTAL / DEPRECATED / DUPLICATE_SUSPECT / DELETE_CANDIDATE / BLOCKED_UNKNOWN_CONSUMER / ARCHIVED |
| `risk` | high / medium / low / blocked |
| `next_action` | KEEP / REGISTER_ONLY / ADD_TEST / EXTRACT_SHARED_HELPER / MERGE_WITH_CANONICAL / DEPRECATE_WITH_NOTICE / DELETE_AFTER_PROOF / BLOCKED_NEEDS_OWNER / BLOCKED_NEEDS_CONSUMER_AUDIT |

---

## Section 1 — Services FastAPI (entrées production)

| code_id | path | role | status | entrypoint | imported_by | tests | risk | next_action |
|---|---|---|---|---|---|---|---|---|
| `webhook_server` | `webhook_server.py` | runtime | ACTIVE | `python3 webhook_server.py` | TradingView (externe) | `tests/test_*.py` | high | KEEP |
| `perf_app` | `perf/perf_app.py` | runtime | ACTIVE | `python3 perf/perf_app.py` | Desk Pro | — | high | KEEP |
| `bitget_bridge_entrypoint` | `bitget_bridge.py` | wrapper | ACTIVE | `python3 bitget_bridge.py` | ops CLI | — | high | KEEP |

---

## Section 2 — Moteurs runtime (coeur pipeline)

| code_id | path | role | status | entrypoint | imported_by | tests | risk | next_action | duplicate_group |
|---|---|---|---|---|---|---|---|---|---|
| `risk_engine` | `modules/risk_engine/app/risk_engine.py` | runtime | ACTIVE | oui | decision_engine, webhook_server | `tests/test_risk_*.py` | high | KEEP | — |
| `risk_calculator` | `modules/risk_engine/app/risk_calculator.py` | helper | ACTIVE | non | risk_engine | — | high | KEEP | — |
| `execution_engine` | `modules/execution_engine/app/execution_engine.py` | runtime | ACTIVE | oui | risk_engine | — | high | KEEP | — |
| `execution_engine_executor` | `modules/execution_engine/executor.py` | runtime | ACTIVE | non | webhook_server | — | high | KEEP | — |
| `position_engine` | `modules/position_engine/app/position_engine.py` | runtime | ACTIVE | oui | execution_engine | — | high | KEEP | — |
| `position_manager` | `modules/position_engine/position_manager.py` | helper | ACTIVE | non | position_engine | — | high | KEEP | — |
| `decision_engine` | `modules/decision_engine/app/decision_engine.py` | runtime | ACTIVE | oui | webhook_server | — | high | KEEP | — |
| `strategy_logic` | `modules/decision_engine/app/strategy_logic.py` | runtime | ACTIVE | non | decision_engine | — | high | KEEP | — |
| `journal_engine` | `modules/journal_engine/app/journal_engine.py` | runtime | ACTIVE | oui | position_engine | — | medium | KEEP | — |
| `perf_engine` | `modules/perf_engine/app/perf_engine.py` | runtime | ACTIVE | oui | perf_app | — | high | KEEP | — |
| `perf_engine_compat_wrapper` | `modules/perf/engine/app/perf_engine.py` | wrapper | CANDIDATE | non | unknown | — | medium | REGISTER_ONLY | D01 |
| `engines_router` | `modules/engines/router.py` | runtime | ACTIVE | non | health/checker | — | high | KEEP | D03 |
| `signal_router` | `modules/signal_router/` | adapter | ACTIVE | — | decision_engine | `tests/signal_router/` | medium | KEEP | — |
| `trade_executor_executor` | `modules/trade_executor/app/__main__.py` | cli | ACTIVE | oui | dry_run_pipeline | `tests/trade_executor/` | high | KEEP | — |
| `trade_executor_impl` | `modules/trade_executor/app/executor.py` | runtime | ACTIVE | non | dry_run_pipeline, result_tracker | `tests/trade_executor/` | high | KEEP | — |

---

## Section 3 — Trading Lab / Realtime V1

| code_id | path | role | status | entrypoint | tests | risk | next_action |
|---|---|---|---|---|---|---|---|
| `trading_lab_v1` | `modules/trading_lab_v1/app/trading_lab_v1.py` | runtime | ACTIVE | oui | — | high | KEEP |
| `trading_lab_comparator_v1` | `modules/trading_lab_v1/app/comparator_v1.py` | runtime | ACTIVE | oui | — | high | KEEP |
| `trading_lab_live_export_v1` | `modules/trading_lab_v1/app/live_export_v1.py` | runtime | ACTIVE | oui | — | high | KEEP |
| `trading_lab_live_obs_v1` | `modules/trading_lab_v1/app/live_observation_v1.py` | runtime | ACTIVE | oui | — | high | KEEP |
| `trading_lab_report_export_v1` | `modules/trading_lab_v1/app/report_export_v1.py` | runtime | ACTIVE | oui | — | medium | KEEP |
| `trading_lab_v1_backups` | `modules/trading_lab_v1/_backups/` | unknown | ARCHIVED | non | — | low | REGISTER_ONLY |
| `trading_realtime_v1` | `modules/trading_realtime_v1/app/trading_realtime_v1.py` | runtime | ACTIVE | oui | — | high | KEEP |
| `trading_realtime_runtime_loop_v1` | `modules/trading_realtime_v1/app/runtime_loop_v1.py` | runtime | ACTIVE | oui | — | high | KEEP |
| `trading_realtime_event_bridge_v1` | `modules/trading_realtime_v1/app/event_bridge_v1.py` | runtime | ACTIVE | oui | — | high | KEEP |
| `trading_realtime_guardrails_v1` | `modules/trading_realtime_v1/app/guardrails_v1.py` | runtime | ACTIVE | oui | — | high | KEEP |
| `trading_realtime_timer_v1` | `modules/trading_realtime_v1/app/timer_v1.py` | runtime | ACTIVE | oui | — | medium | KEEP |
| `trading_realtime_export_v1` | `modules/trading_realtime_v1/app/export_v1.py` | runtime | ACTIVE | oui | — | medium | KEEP |
| `trading_realtime_reporting_v1` | `modules/trading_realtime_v1/app/reporting_v1.py` | runtime | ACTIVE | oui | — | medium | KEEP |

---

## Section 4 — Desk Pro / Vision

| code_id | path | role | status | entrypoint | tests | risk | next_action |
|---|---|---|---|---|---|---|---|
| `desk_pro_runner` | `modules/desk_pro_runner/app/desk_pro_runner.py` | orchestrator | ACTIVE | oui | — | medium | KEEP |
| `desk_pro_orchestrator` | `modules/desk_pro_orchestrator/app/desk_pro_orchestrator.py` | orchestrator | ACTIVE | oui | — | medium | KEEP |
| `desk_pro_dashboard` | `modules/desk_pro_dashboard/app/desk_pro_dashboard.py` | runtime | ACTIVE | oui | — | medium | KEEP |
| `desk_pro_api_routes` | `modules/desk_pro/api/routes.py` | runtime | ACTIVE | non | perf_app | — | medium | KEEP |
| `desk_state` | `modules/desk_state/desk_state.py` | runtime | ACTIVE | oui | — | medium | KEEP |
| `desk_analyze` | `modules/desk_analyze/analyze_latest.py` | cli | ACTIVE | oui | — | low | KEEP |
| `desk_snapshot_ingest` | `modules/desk_snapshot_ingest/ingest_snapshots.py` | cli | ACTIVE | oui | — | medium | KEEP |
| `vision_bot` | `modules/vision_bot/app/vision_bot.py` | runtime | ACTIVE | oui | — | medium | KEEP |
| `bot_vision_step2` | `modules/bot_vision_step2/app/bot_vision_step2.py` | runtime | ACTIVE | oui | — | medium | KEEP |
| `bot_vision_step1` | `modules/bot_vision/bot_vision_step1/` | runtime | CANDIDATE | — | — | low | BLOCKED_NEEDS_OWNER |

---

## Section 5 — Collecteurs

| code_id | path | role | status | entrypoint | tests | risk | next_action |
|---|---|---|---|---|---|---|---|
| `collector_binance_spot_cli` | `modules/collector_binance_spot/src/collector_binance_spot/cli.py` | collector | ACTIVE | oui | `modules/collector_binance_spot/tests/` | medium | KEEP |
| `collector_coingecko_cli` | `modules/collector_coingecko/src/collector_coingecko/cli.py` | collector | ACTIVE | oui | `modules/collector_coingecko/tests/` | medium | KEEP |
| `derivatives_collector` | `modules/derivatives_collector/app/derivatives_collector.py` | collector | ACTIVE | oui | `modules/derivatives_collector/tests/` | medium | KEEP |
| `derivatives_collector_compat` | `modules/derivatives_collector/app/lifecycle_compat.py` | adapter | ACTIVE | oui | — | medium | KEEP |
| `market_metrics_v1` | `modules/derivatives_collector/app/market_metrics_v1.py` | runtime | ACTIVE | non | `tests/test_market_metrics_v1.py` | medium | KEEP |
| `derivatives_analyzer` | `modules/derivatives_analyzer/app/derivatives_analyzer.py` | runtime | ACTIVE | oui | — | medium | KEEP |
| `liquidation_analyzer` | `modules/liquidation_analyzer/app/liquidation_analyzer.py` | runtime | ACTIVE | oui | — | medium | KEEP |
| `market_scanner` | `modules/market_scanner/app/market_scanner.py` | runtime | ACTIVE | oui | — | medium | KEEP |

---

## Section 6 — Openclaw / Agents

| code_id | path | role | status | entrypoint | tests | risk | next_action |
|---|---|---|---|---|---|---|---|
| `openclaw_operator_bridge` | `modules/openclaw_operator_bridge/app/__main__.py` | cli | ACTIVE | oui | `modules/openclaw_operator_bridge/tests/` | medium | KEEP |
| `openclaw_tmux_health` | `modules/openclaw_tmux_operator/scripts/health_aggregate.py` | cli | ACTIVE | oui | `tests/openclaw_tmux_operator/` | low | KEEP |
| `memory_bricks_api` | `modules/memory_bricks/app/api_v2_server.py` | runtime | ACTIVE | oui | — | medium | KEEP |
| `memory_bricks_cli` | `modules/memory_bricks/src/memory_bricks_v1/cli.py` | cli | ACTIVE | oui | `modules/memory_bricks/tests/` | low | KEEP |
| `validated_prompt_factory` | `modules/validated_prompt_factory/app/validated_prompt_factory.py` | runtime | ACTIVE | oui | — | low | KEEP |
| `model_provider_openclaw` | `modules/model_provider_openclaw/app/model_provider_openclaw.py` | runtime | ACTIVE | oui | — | low | KEEP |
| `mcp_policy_validator` | `modules/governance/openclaw_mcp_policy_validator/__main__.py` | validator | ACTIVE | oui | `tests/openclaw/` | medium | KEEP |

---

## Section 7 — Validateurs et schémas

| code_id | path | role | status | entrypoint | tests | risk | next_action |
|---|---|---|---|---|---|---|---|
| `validate_master_target_continuity` | `tools/governance/validate_master_target_continuity.py` | validator | ACTIVE | oui | — | medium | ADD_TEST |
| `validate_policy_json_report_schema` | `tools/openclaw/validate_policy_json_report_schema.py` | validator | ACTIVE | oui | `tests/openclaw/test_validate_policy_json_report_schema.py` | medium | KEEP |
| `validate_runtime_security_all` | `tools/openclaw/validate_runtime_security_all.py` | validator | ACTIVE | oui | `tests/openclaw/test_validate_runtime_security_all.py` | medium | KEEP |
| `validate_skill_policy_static` | `tools/openclaw/validate_skill_policy_static.py` | validator | ACTIVE | oui | `tests/openclaw/test_validate_skill_policy_static.py` | medium | KEEP |
| `validate_strategy_registry` | `tools/strategy/validate_strategy_registry.py` | validator | ACTIVE | oui | — | medium | ADD_TEST |
| `validation_gate` | `modules/validation_gate/app/__main__.py` | validator | ACTIVE | oui | `modules/validation_gate/tests/test_gate.py` | high | KEEP |
| `webhook_key_validator` | `modules/auth/webhook_key.py` | validator | ACTIVE | non | — | high | KEEP |
| `why_lint_static_validator` | `tools/why_lint_static_validator/why_lint_static_validator.py` | validator | ACTIVE | oui | — | low | KEEP |
| `schema_webhook_event_v1` | `schemas/webhook_event_v1.json` | schema | ACTIVE | non | partiel | high | KEEP |
| `schema_trading_event_v1` | `docs/ot/trading/schemas/trading_event_v1.schema.json` | schema | ACTIVE | non | — | high | ADD_TEST |
| `schema_trading_trade_v1` | `docs/ot/trading/schemas/trading_trade_v1.schema.json` | schema | ACTIVE | non | — | high | ADD_TEST |

---

## Section 8 — Infra / Fleet / Santé

| code_id | path | role | status | entrypoint | tests | risk | next_action |
|---|---|---|---|---|---|---|---|
| `health_checker` | `modules/health/checker.py` | validator | ACTIVE | oui | — | medium | KEEP |
| `healthcheck` | `modules/runtime_health/healthcheck.py` | cli | ACTIVE | oui | `tests/runtime_health/` | medium | KEEP |
| `fleet_orchestrator` | `modules/runtime_health/fleet_orchestrator.py` | orchestrator | ACTIVE | oui | — | medium | KEEP |
| `git_fleet_guard` | `modules/git_fleet_guard/app/git_fleet_guard.py` | cli | ACTIVE | oui | — | medium | KEEP |
| `notification_dispatcher` | `modules/notification_dispatcher/app/__main__.py` | cli | ACTIVE | oui | `modules/notification_dispatcher/tests/` | medium | KEEP |
| `localcms` | `modules/localcms/` | runtime | ACTIVE | — | `tests/test_localcms.py` | medium | KEEP |

---

## Section 9 — Registry readers

| code_id | path | role | status | entrypoint | risk | next_action |
|---|---|---|---|---|---|---|
| `registry_meta_reader` | `modules/registry_meta_reader/app/registry_meta_reader.py` | cli | ACTIVE | oui | low | KEEP |
| `registry_router` | `modules/registry_router/app/registry_router.py` | cli | ACTIVE | oui | low | KEEP |
| `modules_registry_reader` | `modules/modules_registry_reader/app/modules_registry_reader.py` | cli | ACTIVE | oui | low | KEEP |
| `wrappers_registry_reader` | `modules/wrappers_registry_reader/app/wrappers_registry_reader.py` | cli | ACTIVE | oui | low | KEEP |
| `machines_registry_reader` | `modules/machines_registry_reader/app/machines_registry_reader.py` | cli | ACTIVE | oui | low | KEEP |
| `naming_normalizer` | `modules/naming_normalizer/app/cli.py` | cli | ACTIVE | oui | low | KEEP |

---

## Section 10 — GitHub Actions workflows

| code_id | path | role | status | déclencheur | risk | next_action |
|---|---|---|---|---|---|---|
| `ci_gated_pr` | `.github/workflows/gated-pr.yml` | validator | ACTIVE | pull_request | high | KEEP |
| `ci_registry_validation` | `.github/workflows/gh-actions-registry-validation.yml` | validator | ACTIVE | push/PR | medium | KEEP |
| `ci_mcp_policy_validator` | `.github/workflows/openclaw-mcp-policy-static-validator.yml` | validator | ACTIVE | push/PR | medium | KEEP |
| `ci_skill_policy_warning` | `.github/workflows/openclaw-skill-policy-warning-only.yml` | validator | ACTIVE | push/PR | low | KEEP |
| `ci_strict_workers_schedule` | `.github/workflows/strict-workers-schedule.yml` | runtime | ACTIVE | schedule | medium | KEEP |
| `ci_strict_workers_smoke` | `.github/workflows/strict-workers-smoke.yml` | validator | ACTIVE | push/PR | medium | KEEP |
| `ci_strict_workers_validate` | `.github/workflows/strict-workers-validate.yml` | validator | ACTIVE | push/PR | medium | KEEP |

---

## Section 11 — Entrées BLOCKED / à qualifier

| code_id | path | status | raison | next_action |
|---|---|---|---|---|
| `router_module_shell` | `modules/router/` | CANDIDATE | facade CLI wrapper (info/readme/ls/grep/menu) — pas de logique Python — FALSE_POSITIVE doublon | KEEP |
| `trae_module_validator` | `modules/trae_module_validator/` | CANDIDATE | ops_menu_hub/scripts/menu.sh:152,162 — entrée menu `menu-trae_module_validator` | KEEP |
| `portfolio_engine` | `modules/portfolio_engine/app/portfolio_engine.py` | ACTIVE | desk_pro_orchestrator:44 (import dynamique) + desk_pro_dashboard | KEEP |
| `probability_engine` | `modules/probability_engine/app/probability_engine.py` | ACTIVE | desk_pro_orchestrator:36 (import dynamique) + proposition_engine/engines.py:17-19 | KEEP |
| `reseau_ssh_step1b` | `modules/reseau_ssh_step1b/` | CANDIDATE | reseau_ssh/scripts/_reseau_ssh_common.sh:35 — RESEAU_SSH_STEP1B_DIR | KEEP |

---

## Section 12 — DELETE_CANDIDATE

| code_id | path | status | preuve requise avant suppression |
|---|---|---|---|
| `install_module_openclaw_bak` | `modules/install_module_openclaw.bak_20260314/` | DELETE_CANDIDATE | grep import négatif confirmé |
| `ops_wrappers_bak` | `modules/ops_wrappers.bak/` | DELETE_CANDIDATE | grep import négatif confirmé |

---

## Section 13 — Anomalies à traiter (lot dédié)

| anomalie_id | description | lot requis |
|---|---|---|
| A01 | 22 modules sans sanity_check.sh | batch sanity_check missing |
| A02 | execution_engine/scripts/ — scripts doublés différents | GO_CODE_OPS_OPT_TRADING_CHILD_DEDUP_AUDIT_01 |
| A03 | modules/router/ — facade CLI wrapper, FALSE_POSITIVE confirmé | registre corrigé — KEEP |
| A04 | validate_master_target_continuity.py sans test | DONE — tests/governance/test_master_target_validator.py (4 PASS) |
| A05 | validate_strategy_registry.py sans test | DONE — tests/governance/test_strategy_registry_validator.py (5 PASS) |
| A06 | schemas S02+S03 sans test de validation | DONE — tests/governance/test_trading_schemas.py (10 PASS) |

---

## Statistiques v1

| Catégorie | Entrées |
|---|---|
| ACTIVE | ~62 |
| CANDIDATE | 4 |
| BLOCKED_UNKNOWN_CONSUMER | 0 |
| DELETE_CANDIDATE | 2 |
| ARCHIVED | 1 |
| DELETED (D05) | 3 |
| **Total** | **~72** |

> Dernière mise à jour 2026-05-28 : D05 supprimé (commit ce0648db) ; A03 corrigé CANDIDATE/KEEP ; T03-T06 BLOCKED qualifiés (4→0) ; A04-A06 tests créés.

Scope non encore enregistré (entrées LOW) :
- `tools/strategy/*/run_*.py` (backtests)
- `tools/strategy/*/fetch_*.py`
- `modules/*/scripts/cmd.sh` (83 scripts)
- AI workers `scripts/ai/workers/*.py`
- modules deepseek, kil_v1, datasheet_writer, learning_feeder, etc.

Ces entrées seront complétées dans un batch v1.1 ou dans le prochain child GO.
