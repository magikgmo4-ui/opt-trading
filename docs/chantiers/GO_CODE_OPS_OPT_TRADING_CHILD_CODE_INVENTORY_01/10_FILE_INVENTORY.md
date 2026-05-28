---
doc_id: GO_CODE_OPS_OPT_TRADING_CHILD_CODE_INVENTORY_01_FILE_INVENTORY
doc_type: inventory_table
repo: opt-trading
project: opt-trading
module: code_ops
go_id: GO_CODE_OPS_OPT_TRADING_CHILD_CODE_INVENTORY_01
status: open
lifecycle_stage: inventory_complete
topic_keys: [code_inventory, file_inventory, audit_first, no_mutation]
surface: docs/chantiers
source_kind: canonical
updated_at: 2026-05-28
---

# 10_FILE_INVENTORY

Inventaire réel du code `opt-trading` — scan du 2026-05-28.

Aucune mutation. Tables produites par `git ls-files` + grep ciblé.

## Résumé des surfaces scannées

| Surface | Fichiers .py | Fichiers .sh | Notes |
|---|---|---|---|
| `modules/` | ~420 | ~620 | 83 modules avec cmd.sh |
| `tools/` | 53 | — | backtests + validateurs |
| `tests/` | 65 | — | tests flat + sous-répertoires |
| `scripts/` | ~30 | ~15 | AI workers, e2e, sheets, telegram |
| `.github/workflows/` | — | — | 7 fichiers YAML |
| `config/` | — | — | 1 fichier YAML (machine_runtime_map.yml) |
| **Total estimé** | **543 .py** | **683 .sh** | **hors data/ et artifacts/** |

## Table A — modules runtime (principaux)

Modules sous `modules/` ayant un rôle runtime prouvé.

| path | role | surface | executable | status | risk |
|---|---|---|---|---|---|
| `modules/risk_engine/app/risk_engine.py` | runtime | modules | oui | active | high |
| `modules/risk_engine/app/risk_calculator.py` | runtime | modules | non | active | high |
| `modules/execution_engine/app/execution_engine.py` | runtime | modules | oui | active | high |
| `modules/execution_engine/executor.py` | runtime | modules | non | active | high |
| `modules/position_engine/app/position_engine.py` | runtime | modules | oui | active | high |
| `modules/position_engine/position_manager.py` | runtime | modules | non | active | high |
| `modules/decision_engine/app/decision_engine.py` | runtime | modules | oui | active | high |
| `modules/decision_engine/app/strategy_logic.py` | runtime | modules | non | active | high |
| `modules/journal_engine/app/journal_engine.py` | runtime | modules | oui | active | medium |
| `modules/perf_engine/app/perf_engine.py` | runtime | modules | oui | active | high |
| `modules/perf/app.py` | runtime | modules | oui | active | high |
| `modules/perf/engine/` | runtime | modules | — | active | high |
| `modules/signal_router/` | adapter | modules | — | active | high |
| `modules/engines/router.py` | runtime | modules | oui | active | high |
| `modules/router/` | runtime | modules | — | active | high |
| `modules/env/` | helper | modules | non | active | medium |
| `shared/logger.py` | helper | shared | non | active | medium |
| `shared/telegram_notify.py` | helper | shared | non | active | medium |

## Table A — modules collectors

| path | role | surface | executable | status | risk |
|---|---|---|---|---|---|
| `modules/collector_binance_spot/src/collector_binance_spot/cli.py` | cli | modules | oui | active | medium |
| `modules/collector_coingecko/src/collector_coingecko/cli.py` | cli | modules | oui | active | medium |
| `modules/derivatives_collector/app/derivatives_collector.py` | runtime | modules | oui | active | medium |
| `modules/derivatives_collector/app/lifecycle_compat.py` | adapter | modules | oui | active | medium |
| `modules/derivatives_collector/app/market_metrics_v1.py` | runtime | modules | non | active | medium |
| `modules/derivatives_collector/app/market_metrics_writer.py` | runtime | modules | non | active | medium |
| `modules/derivatives_analyzer/app/derivatives_analyzer.py` | runtime | modules | oui | active | medium |
| `modules/liquidation_analyzer/app/liquidation_analyzer.py` | runtime | modules | oui | active | medium |
| `modules/market_scanner/app/market_scanner.py` | runtime | modules | oui | active | medium |
| `modules/opportunity_ranker/app/opportunity_ranker.py` | runtime | modules | oui | active | low |

## Table A — modules desk / vision

| path | role | surface | executable | status | risk |
|---|---|---|---|---|---|
| `modules/desk_pro_runner/app/desk_pro_runner.py` | runtime | modules | oui | active | medium |
| `modules/desk_pro_orchestrator/app/desk_pro_orchestrator.py` | runtime | modules | oui | active | medium |
| `modules/desk_pro_dashboard/app/desk_pro_dashboard.py` | runtime | modules | oui | active | medium |
| `modules/desk_pro/` | service | modules | — | active | medium |
| `modules/desk_analyze/analyze_latest.py` | cli | modules | oui | active | low |
| `modules/desk_capture_inputs/extract_tv_inputs.py` | cli | modules | oui | active | low |
| `modules/desk_snapshot_ingest/ingest_snapshots.py` | cli | modules | oui | active | medium |
| `modules/desk_state/desk_state.py` | runtime | modules | oui | active | medium |
| `modules/vision_bot/app/vision_bot.py` | runtime | modules | oui | active | medium |
| `modules/bot_vision_step2/app/bot_vision_step2.py` | runtime | modules | oui | active | medium |
| `modules/bot_vision/bot_vision_step1/` | legacy | modules | — | candidate | low |

## Table A — modules openclaw / agents

| path | role | surface | executable | status | risk |
|---|---|---|---|---|---|
| `modules/openclaw_config_modulaire/` | cli | modules | — | active | medium |
| `modules/gateway_openclaw/` | service | modules | — | active | medium |
| `modules/openclaw_operator_bridge/app/__main__.py` | cli | modules | oui | active | medium |
| `modules/openclaw_tmux_operator/scripts/health_aggregate.py` | cli | modules | oui | active | low |
| `modules/validated_prompt_factory/app/validated_prompt_factory.py` | runtime | modules | oui | active | low |
| `modules/model_provider_openclaw/app/model_provider_openclaw.py` | runtime | modules | oui | active | low |
| `modules/memory_bricks/app/api_v2_server.py` | service | modules | oui | active | medium |
| `modules/memory_bricks/src/memory_bricks_v1/cli.py` | cli | modules | oui | active | low |

## Table A — modules governance / registry

| path | role | surface | executable | status | risk |
|---|---|---|---|---|---|
| `modules/governance/openclaw_mcp_policy_validator/__main__.py` | cli | modules | oui | active | medium |
| `modules/governance/openclaw_mcp_policy_validator/cli.py` | cli | modules | oui | active | medium |
| `modules/registry_meta_reader/app/registry_meta_reader.py` | cli | modules | oui | active | low |
| `modules/registry_router/app/registry_router.py` | cli | modules | oui | active | low |
| `modules/modules_registry_reader/app/modules_registry_reader.py` | cli | modules | oui | active | low |
| `modules/wrappers_registry_reader/app/wrappers_registry_reader.py` | cli | modules | oui | active | low |
| `modules/machines_registry_reader/app/machines_registry_reader.py` | cli | modules | oui | active | low |
| `modules/naming_normalizer/app/cli.py` | cli | modules | oui | active | low |

## Table A — modules infra / deploy

| path | role | surface | executable | status | risk |
|---|---|---|---|---|---|
| `modules/health/checker.py` | validator | modules | oui | active | medium |
| `modules/runtime_health/healthcheck.py` | cli | modules | oui | active | medium |
| `modules/runtime_health/fleet_orchestrator.py` | cli | modules | oui | active | medium |
| `modules/git_fleet_guard/app/git_fleet_guard.py` | cli | modules | oui | active | medium |
| `modules/notification_dispatcher/app/__main__.py` | cli | modules | oui | active | medium |
| `modules/localcms/` | service | modules | — | active | medium |
| `modules/reseau_ssh/` | service | modules | — | active | medium |
| `modules/reseau_ssh_step1b/` | service | modules | — | active | unknown |

## Table A — trading lab / realtime

| path | role | surface | executable | status | risk |
|---|---|---|---|---|---|
| `modules/trading_lab_v1/app/trading_lab_v1.py` | runtime | modules | oui | active | high |
| `modules/trading_lab_v1/app/comparator_v1.py` | runtime | modules | oui | active | high |
| `modules/trading_lab_v1/app/live_export_v1.py` | runtime | modules | oui | active | high |
| `modules/trading_lab_v1/app/live_observation_v1.py` | runtime | modules | oui | active | high |
| `modules/trading_lab_v1/app/report_export_v1.py` | runtime | modules | oui | active | medium |
| `modules/trading_lab_v1/_backups/` | archive | modules | non | deprecated | low |
| `modules/trading_realtime_v1/app/trading_realtime_v1.py` | runtime | modules | oui | active | high |
| `modules/trading_realtime_v1/app/runtime_loop_v1.py` | runtime | modules | oui | active | high |
| `modules/trading_realtime_v1/app/event_bridge_v1.py` | runtime | modules | oui | active | high |
| `modules/trading_realtime_v1/app/guardrails_v1.py` | runtime | modules | oui | active | high |
| `modules/trading_realtime_v1/app/timer_v1.py` | runtime | modules | oui | active | medium |
| `modules/trading_realtime_v1/app/export_v1.py` | runtime | modules | oui | active | medium |
| `modules/trading_realtime_v1/app/reporting_v1.py` | runtime | modules | oui | active | medium |

## Table A — racine et services principaux

| path | role | surface | executable | status | risk |
|---|---|---|---|---|---|
| `webhook_server.py` | service | racine | oui | active | high |
| `perf/perf_app.py` | service | racine | oui | active | high |
| `bitget_bridge.py` | adapter | racine | oui | active | high |

## Modules sans sanity_check.sh (22 / 83)

Ces modules ont cmd.sh mais manquent de sanity_check.sh, en violation de la convention
`modules/` définie dans CLAUDE.md.

```text
modules/configure_openclaw
modules/datasheet_writer
modules/dev_validation_hub
modules/doctor_openclaw
modules/evidence_openclaw
modules/gateway_openclaw
modules/install_module_openclaw
modules/learning_feeder
modules/localcms
modules/menu_openclaw
modules/model_provider_openclaw
modules/notification_dispatcher
modules/openclaw_config_modulaire
modules/openclaw_operator_bridge
modules/openclaw_tmux_operator
modules/proposition_engine
modules/result_tracker
modules/signal_router
modules/trade_executor
modules/trading_lab_v1
modules/trading_realtime_v1
modules/validation_gate
```

## Modules à convention non standard

| Module | Anomalie |
|---|---|
| `modules/execution_engine/scripts/` | scripts doublés (cmd.sh + execution_engine_cmd.sh, menu.sh + execution_engine_menu.sh, sanity_check.sh + execution_engine_sanity_check.sh) |
| `modules/reseau_ssh/scripts/` | script reseau_ssh_cmd.sh et reseau_ssh_menu.sh en plus des canoniques |
| `modules/bot_vision/bot_vision_step1/` | structure legacy non standard (scripts sous desk_pro_vision_scripts/) |
| `modules/perf/` | contient engine/ comme sous-répertoire + webhook.py à la racine |
| `modules/install_module_openclaw.bak_20260314/` | répertoire backup présent dans le repo |
| `modules/ops_wrappers.bak/` | répertoire backup présent dans le repo |
