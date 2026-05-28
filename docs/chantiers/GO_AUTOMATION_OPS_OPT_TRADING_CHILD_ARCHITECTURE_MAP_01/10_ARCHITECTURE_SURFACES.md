---
doc_id: GO_AUTOMATION_OPS_OPT_TRADING_CHILD_ARCHITECTURE_MAP_01_SURFACES
doc_type: architecture_surfaces
repo: opt-trading
go_id: GO_AUTOMATION_OPS_OPT_TRADING_CHILD_ARCHITECTURE_MAP_01
updated_at: 2026-05-28
---

# 10_ARCHITECTURE_SURFACES

## Surface 1 — Pipeline trading signal

| Composant | Fichier | Rôle | Port/Persistance |
|---|---|---|---|
| TradingView webhook | externe | émission signal | — |
| `webhook_server.py` | racine | réception + validation | 8000 / `state/events.jsonl` |
| `risk_engine` | `modules/risk_engine/app/` | sizing tier (FULL/HALF/MICRO/NONE) | — |
| `execution_engine` | `modules/execution_engine/app/` | cycle de vie trade | — |
| `position_engine` | `modules/position_engine/app/` | suivi position | — |
| `perf_engine` | `modules/perf_engine/app/` | tracker candidat→actif→clos | — |
| `perf_app` | `perf/perf_app.py` | API exposition résultats | 8010 / `perf/perf.db` |
| `adapters/webhook_to_perf.py` | `adapters/` | normalisation frontière | — |

## Surface 2 — Desk Pro stack

| Composant | Fichier | Rôle |
|---|---|---|
| `desk_pro_runner` | `modules/desk_pro_runner/` | entry point opérateur |
| `desk_pro_orchestrator` | `modules/desk_pro_orchestrator/app/` | orchestration dashboard stack (import dynamique) |
| `desk_pro_dashboard` | `modules/desk_pro_dashboard/app/` | UI données desk |
| `portfolio_engine` | `modules/portfolio_engine/app/` | données portefeuille (consommé par orchestrator + dashboard) |
| `probability_engine` | `modules/probability_engine/app/` | scores probabilistes (consommé par orchestrator + proposition_engine) |
| `localcms` | `modules/localcms/app.py` | cockpit ops lecture-seule | 8700 |

## Surface 3 — OpenClaw ops

| Composant | Fichier | Rôle | Trigger |
|---|---|---|---|
| `gateway_openclaw` | `modules/gateway_openclaw/scripts/` | start/stop/attach/logs session tmux `openclaw-gateway` | manual |
| `openclaw_config_modulaire` | `modules/openclaw_config_modulaire/scripts/` | apply_safe + rollback `~/.openclaw/config.d/` | manual |
| `openclaw_tmux_operator` | `modules/openclaw_tmux_operator/scripts/` | opérations tmux OpenClaw | manual |
| `openclaw_operator_bridge` | `modules/openclaw_operator_bridge/` | pont opérateur ↔ OpenClaw | manual/openclaw_call |

## Surface 4 — GitHub Actions CI/CD

| Workflow | Trigger | Rôle | Python |
|---|---|---|---|
| `gated-pr.yml` | PR → sot/mainline | gate principal | 3.x |
| `gh-actions-registry-validation.yml` | PR (paths) | valide registres GHA YAML | 3.11 |
| `openclaw-mcp-policy-static-validator.yml` | PR (paths) | valide policy MCP OpenClaw | 3.11 |
| `openclaw-skill-policy-warning-only.yml` | PR (paths) | warning-only skill policy | 3.11 |
| `strict-workers-schedule.yml` | cron lun 08:00 | audit strict workers planifié | — |
| `strict-workers-smoke.yml` | PR (paths) | smoke strict workers | — |
| `strict-workers-validate.yml` | PR (paths) | valide job_packets JSON | 3.11 |

## Surface 5 — AI Workers

| Composant | Path | Rôle | Statut |
|---|---|---|---|
| `run_task.sh` | `scripts/ai/workers/run_task.sh` | entry point unique pour tous les job_packets | active |
| `tasks.index.json` | `scripts/ai/workers/tasks.index.json` | index tâches (schema 0.3-draft) | DRAFT_ONLY |
| `models.registry.json` | `scripts/ai/workers/models.registry.json` | registre modèles IA | active |
| `job_packets/` | `scripts/ai/workers/job_packets/*.json` | 30 packets GO-liés | active/candidate |
| `_validate_job.py` | `scripts/ai/workers/` | validateur JSON des packets | active |
| Workers Python | `scripts/ai/workers/*.py` | 26 scripts spécialisés (ledger, doc_ops, health, signal, etc.) | varies |
| `orchestration/` | `scripts/ai/workers/orchestration/` | contrat orchestration externe (DRAFT) | candidate |

### Workers Python par famille

| Famille | Scripts |
|---|---|
| `ledger_*` | ledger_blocked_events_digest, ledger_replay, ledger_rotation_check, ledger_schema_validation, ledger_trace_id_audit, ledger_writer |
| `doc_ops_*` | doc_ops_constraint_check, doc_ops_create_chantier, doc_ops_go_index_insert |
| `strict_worker_*` | strict_worker_denied_command_scan, strict_worker_log_archive, strict_worker_output_schema_check |
| `signal_*` | signal_processor, signal_stats |
| monitoring | health_status, stuck_job_detector, permission_drift_check, oauth_scope_audit |
| repo | repo_doc_frontmatter_lint, repo_doc_link_check |
| ops | kill_switch_fullstop_test, localcms_automation_status_sync, openclaw_mobile_control, runner_readonly |

## Surface 6 — Fleet health

| Composant | Fichier | Rôle |
|---|---|---|
| `runtime_health` | `modules/runtime_health/healthcheck.py` | checks fleet (tmux lecture seule) |
| `fleet_orchestrator` | `modules/runtime_health/fleet_orchestrator.py` | orchestration SSH multi-machine |
| Machines surveillées | cursor-ai (Windows), fantome (Linux) | cibles healthcheck |
| Notification | `shared/telegram_notify.py` | alertes Telegram |

## Surface 7 — Data collectors

| Composant | Fichier | Mode |
|---|---|---|
| `collector_binance_spot` | `modules/collector_binance_spot/` | oneshot, public API |
| `derivatives_collector` | `modules/derivatives_collector/` | OI/Funding/Liquidations via Coinglass |
| `bot_vision_step2` | `modules/bot_vision_step2/` | capture headless opérationnelle |
| `vision_bot` | `modules/vision_bot/` | inbox/outbox ShareX → SFTP → markdown |
