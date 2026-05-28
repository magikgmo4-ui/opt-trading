---
doc_id: GO_CODE_OPS_OPT_TRADING_CHILD_CODE_INVENTORY_01_ENTRYPOINTS
doc_type: inventory_table
repo: opt-trading
project: opt-trading
module: code_ops
go_id: GO_CODE_OPS_OPT_TRADING_CHILD_CODE_INVENTORY_01
status: open
lifecycle_stage: inventory_complete
topic_keys: [entrypoints, cli, code_inventory, audit_first]
surface: docs/chantiers
source_kind: canonical
updated_at: 2026-05-28
---

# 20_ENTRYPOINTS

## Table B — entrypoints CLI et services principaux

### Services FastAPI (runtime permanent)

| command | path | rôle | port | json_parseable | docs | tests |
|---|---|---|---|---|---|---|
| `python3 webhook_server.py` | `webhook_server.py` | TV webhook receptor | 8000 | oui | docs/API.md | tests/test_*.py |
| `python3 perf/perf_app.py` | `perf/perf_app.py` | perf analytics API | 8010 | oui | docs/API.md | — |
| `python3 modules/localcms/app.py` | `modules/localcms/` | LocalCMS cockpit | 8700 | partiel | CLAUDE.md | tests/test_localcms.py |

### Entrypoints runtime (main guard prouvé)

| path | surface | args | output | risk |
|---|---|---|---|---|
| `modules/decision_engine/app/decision_engine.py` | modules | — | events | high |
| `modules/execution_engine/app/execution_engine.py` | modules | — | orders | high |
| `modules/position_engine/app/position_engine.py` | modules | — | positions | high |
| `modules/risk_engine/app/risk_engine.py` | modules | — | sizing | high |
| `modules/trading_lab_v1/app/trading_lab_v1.py` | modules | — | report | high |
| `modules/trading_realtime_v1/app/trading_realtime_v1.py` | modules | — | runtime | high |
| `modules/desk_pro_runner/app/desk_pro_runner.py` | modules | — | dashboard | medium |
| `modules/desk_pro_orchestrator/app/desk_pro_orchestrator.py` | modules | — | orchestration | medium |
| `modules/desk_pro_dashboard/app/desk_pro_dashboard.py` | modules | — | UI | medium |
| `modules/perf_engine/app/perf_engine.py` | modules | — | perf data | high |
| `modules/vision_bot/app/vision_bot.py` | modules | — | artefacts | medium |
| `modules/bot_vision_step2/app/bot_vision_step2.py` | modules | — | Telegram | medium |
| `modules/journal_engine/app/journal_engine.py` | modules | — | journal | medium |
| `modules/memory_bricks/app/api_v2_server.py` | modules | — | API | medium |
| `modules/git_fleet_guard/app/git_fleet_guard.py` | modules | — | fleet status | medium |
| `bitget_bridge.py` | racine | — | orders | high |

### Entrypoints CLI (argparse / click / typer détecté)

| path | surface | args | output | risk |
|---|---|---|---|---|
| `modules/collector_binance_spot/src/collector_binance_spot/cli.py` | modules | — | JSON | medium |
| `modules/collector_coingecko/src/collector_coingecko/cli.py` | modules | — | JSON | medium |
| `modules/derivatives_collector/app/derivatives_collector.py` | modules | — | JSON | medium |
| `modules/derivatives_collector/app/lifecycle_compat.py` | modules | — | JSON | medium |
| `modules/kil_v1/src/kil_v1/cli.py` | modules | — | JSON | low |
| `modules/memory_bricks/src/memory_bricks_v1/cli.py` | modules | — | JSON | low |
| `modules/naming_normalizer/app/cli.py` | modules | — | stdout | low |
| `modules/governance/openclaw_mcp_policy_validator/cli.py` | modules | — | JSON | medium |
| `modules/desk_pro/ui/page.py` | modules | — | HTML | medium |
| `modules/desk_pro/api/routes.py` | modules | — | JSON | medium |
| `modules/engines/router.py` | modules | — | routing | high |
| `modules/datasheet_writer/app/__main__.py` | modules | — | sheets | medium |
| `modules/learning_feeder/app/__main__.py` | modules | — | feed | low |
| `modules/notification_dispatcher/app/__main__.py` | modules | — | notify | medium |
| `modules/openclaw_operator_bridge/app/__main__.py` | modules | — | bridge | medium |
| `modules/proposition_engine/app/__main__.py` | modules | — | prompts | low |
| `modules/result_tracker/app/__main__.py` | modules | — | tracking | low |
| `modules/trade_executor/app/__main__.py` | modules | — | orders | high |
| `modules/validation_gate/app/__main__.py` | modules | — | validation | high |

### Entrypoints tools (backtests + validateurs)

| path | surface | args | output | risk |
|---|---|---|---|---|
| `tools/strategy/dca_spot/run_backtest.py` | tools | — | results | low |
| `tools/strategy/dca_capital/run_comparison.py` | tools | — | results | low |
| `tools/strategy/dca_capital/run_v2_grid.py` | tools | — | results | low |
| `tools/strategy/dca_cfd_short/run_cfd_grid.py` | tools | — | results | low |
| `tools/strategy/dca_cfd_short/run_eval.py` | tools | — | results | low |
| `tools/strategy/daily_scalping/run_backtest.py` | tools | — | results | low |
| `tools/governance/validate_master_target_continuity.py` | tools | — | pass/fail | medium |
| `tools/openclaw/validate_policy_json_report_schema.py` | tools | — | pass/fail | medium |
| `tools/openclaw/validate_runtime_security_all.py` | tools | — | pass/fail | medium |
| `tools/openclaw/validate_skill_policy_static.py` | tools | — | pass/fail | medium |
| `tools/strategy/validate_strategy_registry.py` | tools | — | pass/fail | medium |

### Entrypoints scripts AI workers

| path | surface | rôle | risk |
|---|---|---|---|
| `scripts/ai/workers/doc_ops_create_chantier.py` | scripts | création chantier | medium |
| `scripts/ai/workers/doc_ops_go_index_insert.py` | scripts | insertion GO index | medium |
| `scripts/ai/workers/doc_ops_constraint_check.py` | scripts | contrainte doc ops | medium |
| `scripts/ai/workers/health_status.py` | scripts | health check | low |
| `scripts/ai/workers/ledger_writer.py` | scripts | ledger write | medium |
| `scripts/ai/workers/ledger_replay.py` | scripts | ledger replay | medium |
| `scripts/ai/workers/signal_stats.py` | scripts | signal stats | low |
| `scripts/ai/workers/runner_readonly.py` | scripts | lecture seule | low |
| `scripts/ai/workers/openclaw_mobile_control.py` | scripts | mobile control | medium |

### GitHub Actions workflows

| file | déclencheur | rôle | risk |
|---|---|---|---|
| `.github/workflows/gated-pr.yml` | pull_request | gate PR | high |
| `.github/workflows/gh-actions-registry-validation.yml` | push/PR | registry validation | medium |
| `.github/workflows/openclaw-mcp-policy-static-validator.yml` | push/PR | MCP policy | medium |
| `.github/workflows/openclaw-skill-policy-warning-only.yml` | push/PR | skill policy | low |
| `.github/workflows/strict-workers-schedule.yml` | schedule | workers périodiques | medium |
| `.github/workflows/strict-workers-smoke.yml` | push/PR | smoke workers | medium |
| `.github/workflows/strict-workers-validate.yml` | push/PR | validation workers | medium |

## Entrypoints suspects / anomalies

| path | anomalie | action recommandée |
|---|---|---|
| `modules/execution_engine/executor.py` | executor à la racine du module EN PLUS de app/ | qualifier doublon vs trade_executor |
| `modules/trade_executor/app/executor.py` | executor.py également dans trade_executor | qualifier doublon |
| `modules/perf/app.py` | FastAPI service direct dans perf/ | clarifier relation avec perf_engine |
| `modules/perf/engine/` | sous-répertoire engine dans perf/ | clarifier relation avec modules/perf_engine/ |
| `deploy_module_multi_machine/app/deploy_module_multi_machine.py` | hors modules/ | noter périmètre isolé |
| `producer_repo_kg_v1.py` | à la racine repo | noter usage |
