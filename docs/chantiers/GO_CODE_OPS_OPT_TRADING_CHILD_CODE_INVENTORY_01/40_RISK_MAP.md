---
doc_id: GO_CODE_OPS_OPT_TRADING_CHILD_CODE_INVENTORY_01_RISK_MAP
doc_type: inventory_table
repo: opt-trading
project: opt-trading
module: code_ops
go_id: GO_CODE_OPS_OPT_TRADING_CHILD_CODE_INVENTORY_01
status: open
lifecycle_stage: inventory_complete
topic_keys: [risk_map, code_inventory, audit_first, no_mutation]
surface: docs/chantiers
source_kind: canonical
updated_at: 2026-05-28
---

# 40_RISK_MAP

Carte de risque du code `opt-trading` pour orienter le refactor par batch.

Critères de risque issus du protocole `10_CODE_INVENTORY_PROTOCOL.md` :

| Niveau | Définition |
|---|---|
| `high` | entrypoint CLI, CI, runtime, stratégie, sécurité, ou ingestion |
| `medium` | utilisé par un runbook ou un autre module |
| `low` | fichier isolé, testé, sans consommateur externe connu |
| `blocked` | consommateur inconnu ou risque de casse non borné |

---

## Zone HIGH — ne pas modifier sans test de verrouillage préalable

| path | raison | consommateurs connus |
|---|---|---|
| `webhook_server.py` | entrée principale TradingView → pipeline | TradingView alerts, `state/events.jsonl` |
| `perf/perf_app.py` | service perf FastAPI | Desk Pro, perf.db |
| `bitget_bridge.py` | pont broker Bitget | orders runtime |
| `modules/risk_engine/app/risk_engine.py` | décision FULL/HALF/MICRO/NONE | decision_engine, execution_engine |
| `modules/risk_engine/app/risk_calculator.py` | calcul sizing | risk_engine.py |
| `modules/execution_engine/app/execution_engine.py` | exécution ordres | risk_engine → position_engine |
| `modules/execution_engine/executor.py` | executor interne | execution_engine.py |
| `modules/position_engine/app/position_engine.py` | lifecycle positions | execution_engine → journal |
| `modules/decision_engine/app/decision_engine.py` | signaux GO_LONG/GO_SHORT | risk_engine |
| `modules/decision_engine/app/strategy_logic.py` | config signal hardcodée | decision_engine |
| `modules/trading_lab_v1/app/trading_lab_v1.py` | LAB V1 | comparator, live_export |
| `modules/trading_lab_v1/app/comparator_v1.py` | comparaison LAB/REALTIME | trading_lab_v1 |
| `modules/trading_realtime_v1/app/trading_realtime_v1.py` | REALTIME V1 | runtime_loop, event_bridge |
| `modules/trading_realtime_v1/app/runtime_loop_v1.py` | boucle runtime | trading_realtime_v1 |
| `modules/trading_realtime_v1/app/event_bridge_v1.py` | pont événements | runtime_loop |
| `modules/trading_realtime_v1/app/guardrails_v1.py` | guardrails sécurité | runtime_loop |
| `modules/perf_engine/app/perf_engine.py` | tracker positions intermédiaires | perf_app.py |
| `modules/engines/router.py` | routeur moteurs | inconnu — BLOCKED |
| `.github/workflows/gated-pr.yml` | gate CI toutes PRs | CI pipeline |
| `modules/validation_gate/app/__main__.py` | gate de validation | CI, AI workers |
| `modules/auth/webhook_key.py` | validation signature webhook | webhook_server.py |

---

## Zone MEDIUM — modifier avec test ou revue

| path | raison | consommateurs connus |
|---|---|---|
| `modules/signal_router/` | routage signaux | decision_engine ou webhook |
| `modules/journal_engine/app/journal_engine.py` | journal des événements | position_engine |
| `modules/desk_pro_runner/app/desk_pro_runner.py` | orchestration Desk Pro | desk_pro_orchestrator |
| `modules/desk_pro_orchestrator/app/desk_pro_orchestrator.py` | orchestration dashboard | desk_pro_runner |
| `modules/desk_pro/api/routes.py` | API Desk Pro | perf_app.py |
| `modules/localcms/` | cockpit LocalCMS | ops locale |
| `modules/memory_bricks/app/api_v2_server.py` | API mémoire | AI workers, openclaw |
| `modules/health/checker.py` | health check | CI, runtime_health |
| `modules/runtime_health/healthcheck.py` | healthcheck fleet | CI, ops |
| `modules/runtime_health/fleet_orchestrator.py` | orchestration fleet | ops |
| `modules/git_fleet_guard/app/git_fleet_guard.py` | guard fleet git | CI, ops |
| `modules/notification_dispatcher/app/__main__.py` | dispatcher notifications | Telegram, ops |
| `modules/derivatives_collector/app/derivatives_collector.py` | collecteur OI/FR | headless, coinglass |
| `modules/vision_bot/app/vision_bot.py` | pipeline vision | ShareX → markdown |
| `modules/bot_vision_step2/app/bot_vision_step2.py` | step 2 vision | Telegram, Desk Pro |
| `.github/workflows/strict-workers-*.yml` | workers CI stricts | AI workers |
| `modules/governance/openclaw_mcp_policy_validator/` | policy MCP | CI, openclaw |
| `modules/openclaw_operator_bridge/app/__main__.py` | bridge operator | openclaw |
| `modules/trade_executor/app/__main__.py` | exécuteur trades | execution_engine ou indépendant ? |
| `scripts/ai/workers/doc_ops_*.py` | workers doc ops | CI gated-pr |

---

## Zone LOW — modifiable avec précaution standard

| path | raison |
|---|---|
| `tools/strategy/*/run_*.py` | backtests, n'affectent pas le runtime |
| `tools/strategy/validate_strategy_registry.py` | validateur statique |
| `modules/naming_normalizer/app/cli.py` | outil standalone |
| `modules/registry_meta_reader/`, `modules_registry_reader/`, `wrappers_registry_reader/` | readers read-only |
| `modules/opportunity_ranker/app/opportunity_ranker.py` | ranker standalone |
| `modules/kil_v1/src/kil_v1/cli.py` | CLI utilitaire |
| `modules/memory_bricks/src/memory_bricks_v1/cli.py` | CLI read-only |
| `modules/desk_analyze/analyze_latest.py` | analyse locale |

---

## Zone BLOCKED — consommateur inconnu ou risque non borné

| path | raison | action |
|---|---|---|
| `modules/engines/router.py` | rôle exact inconnu dans le flux actuel | qualifier avant tout refactor |
| `modules/router/` | relation avec engines/router.py inconnue | qualifier doublon ou séparation |
| `modules/trae_module_validator/` | rôle non documenté | qualifier et documenter |
| `modules/reseau_ssh_step1b/` | relation avec reseau_ssh/ non documentée | qualifier |
| `modules/portfolio_engine/app/portfolio_engine.py` | consommateurs non identifiés | qualifier |
| `modules/probability_engine/app/probability_engine.py` | consommateurs non identifiés | qualifier |
| `modules/simex_bitget_bridge/app/simex_bitget_bridge.py` | relation avec bitget_bridge.py | qualifier doublon |
| `modules/perf/engine/` | relation avec modules/perf_engine/ | qualifier doublon |

---

## Doublons suspects identifiés (résumé)

| id | paths | type suspect | décision requise |
|---|---|---|---|
| D01 | `modules/perf/engine/` + `modules/perf_engine/app/perf_engine.py` | duplication fonctionnelle probable | qualifier avant refactor |
| D02 | `modules/execution_engine/executor.py` + `modules/trade_executor/app/executor.py` | rôle executor similaire | qualifier consommateurs |
| D03 | `modules/engines/router.py` + `modules/router/` | routeurs potentiellement redondants | qualifier |
| D04 | `modules/simex_bitget_bridge/` + `bitget_bridge.py` | bridges Bitget | qualifier rôles distincts |
| D05 | `modules/execution_engine/scripts/execution_engine_cmd.sh` + `modules/execution_engine/scripts/cmd.sh` | scripts doublés dans même module | supprimer les doublés aliasés |
| D06 | `modules/install_module_openclaw.bak_20260314/` + `modules/ops_wrappers.bak/` | répertoires .bak dans repo | retirer ou archiver |

---

## Surfaces non scannées (hors périmètre protocole)

| surface | raison d'exclusion |
|---|---|
| `data/` | données lourdes hors refactor |
| `artifacts/` | sorties générées |
| `bundles/` | archives transport |
| `docs/` | documentation (hors runbooks CLI) |
| `registry/` | dérivé machine-readable |
| `_archive/` | historique |
