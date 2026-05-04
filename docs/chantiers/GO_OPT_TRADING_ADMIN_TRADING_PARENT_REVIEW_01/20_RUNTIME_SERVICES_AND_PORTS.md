---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_PARENT_REVIEW_01_SERVICES_PORTS
doc_type: services_ports_map
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_PARENT_REVIEW_01
status: active
surface: chantier
source_kind: canonical
updated_at: 2026-05-04
---

# 20_RUNTIME_SERVICES_AND_PORTS — admin-trading

Etat controle le 2026-05-04 via SSH read-only. Aucun service modifie.

## Services systemd — etat reel

### ACTIFS + RUNNING

| Service | PID | User | Port | Description |
| --- | --- | --- | --- | --- |
| tv-webhook.service | 1466 | ghost | 0.0.0.0:8000 | TradingView Webhook (FastAPI/Uvicorn) |
| tv-perf.service | 796 | root | 0.0.0.0:8010 | Trading Perf API (FastAPI/Uvicorn) |
| vision_bot.service | 798 | ghost | - | ShareX inbox -> outbox watch loop |
| bot_vision_step2.service | 1463 | ghost | - | Telegram /analyze -> Desk Pro artifacts |
| ngrok-tv.service | 1492 | - | 127.0.0.1:4040 | ngrok tunnel pour TradingView |

### FAILED (non bloquants)

| Service | Raison |
| --- | --- |
| desk_bridge.service | Erreur PIL sur image corrompue (screen_2026-03-06). Input problem, pas bug runtime. |
| macro-xau.service | /opt/trading/jobs/macro_xau/run.sh manquant. Module non deploye. |

### INACTIFS (normaux pour timers oneshot)

| Service/Timer | Statut |
| --- | --- |
| bot_vision_step2_prune.timer | enabled (oneshot, deja execute) |
| desk_retention.timer | enabled (oneshot, deja execute) |
| trading-heartbeat.timer | disabled |
| bot_vision_step2_send.timer | disabled |

### UNIT FILES

| Fichier | Enabled |
| --- | --- |
| tv-webhook.service | enabled |
| tv-perf.service | enabled |
| vision_bot.service | enabled |
| bot_vision_step2.service | enabled |
| ngrok-tv.service | enabled |
| desk_bridge.service | static |
| desk_retention.service | static |
| trading-heartbeat.service | disabled |
| perf.service | masked (remplace par tv-perf) |

## Ports en ecoute

| Port | Interface | Processus | Service |
| --- | --- | --- | --- |
| 22 | 0.0.0.0 + [::] | sshd | SSH |
| 8000 | 0.0.0.0 | python (PID 1466) | tv-webhook |
| 8010 | 0.0.0.0 | python (PID 796) | tv-perf |
| 4040 | 127.0.0.1 | ngrok (PID 1492) | ngrok web UI |
| 4096 | 127.0.0.1 | opencode (PID 113971) | OpenCode IDE |
| 51820 | * | kernel (wg0) | WireGuard principal |
| 51821 | * | kernel (wg-mgmt) | WireGuard management |

Aucun port 8080, 18789, 18790. Pas d'OpenClaw gateway.

## Processus Python actifs

| PID | User | Commande |
| --- | --- | --- |
| 796 | root | uvicorn perf.perf_app:app --host 0.0.0.0 --port 8010 |
| 798 | ghost | python3 vision_bot.py watch |
| 1463 | ghost | python bot_vision_step2.py serve |
| 1466 | ghost | uvicorn webhook_server:app --host 0.0.0.0 --port 8000 |

## Wrapper shortcuts installes

40+ wrappers dans /usr/local/bin/cmd-*, menu-*, sanity-* couvrant :
- desk_pro, desk_pro_runner, desk_pro_dashboard, desk_analyze, desk_capture_inputs
- decision_engine, probability_engine, risk_engine, execution_engine, position_engine
- derivatives_analyzer, derivatives_collector, liquidation_analyzer
- market_scanner, opportunity_ranker, marketdata
- vision_bot, bot_vision_step2
- ops_menu_hub, ops_super, ops_hub
- journal_engine, journal_de_bord, env, audit, auth
- deepseek_hub, deepseek_response, deepseek_student, deepseek_thinking
- modules_registry_reader, machines_registry_reader
- install_module, git_sync_all, infra_context, deploy_module_multi_machine

## Fichiers .env (listes, non lus)

- /opt/trading/.env (principal)
- modules/bot_vision_step2/config/bot_vision.env
- modules/desk_capture_inputs/config/desk_capture_inputs.env
- modules/desk_retention/config/desk_retention.env
- modules/auth/secrets.py
