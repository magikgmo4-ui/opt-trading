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

## Etat observable

admin-trading est unreachable. L'etat ci-dessous est deduit du repo, des registres et des references documentaires. Aucun controle runtime direct n'a ete possible.

## Services systemd attendus

### Services actifs probables

| Service | Module | Description | Statut attendu |
| --- | --- | --- | --- |
| tv-webhook.service | webhook_server.py | Entrypoint FastAPI webhook TradingView | actif |
| ngrok-tv.service | - | Tunnel ngrok pour TradingView | actif (si utilise) |
| vision_bot.service | vision_bot | Watch loop inbox/outbox ShareX -> vision | actif ou arrete |
| bot_vision_step2.service | bot_vision_step2 | Analyse Vision / Telegram | actif ou arrete |
| bot_vision_step2_send.service | bot_vision_step2 | Timer envoi Telegram | timer |
| bot_vision_step2_prune.service | bot_vision_step2 | Timer nettoyage | timer |
| desk_retention.service | desk_retention | Retention donnees historiques | timer |

### Services possibles (non confirmes)

| Service | Module | Notes |
| --- | --- | --- |
| perf.service | perf/perf_app.py | FastAPI perf engine |
| shared_files_sftp | shared_files_sftp | Serveur SFTP /shared |

## Ports attendus

| Port | Service | Protocole | Notes |
| --- | --- | --- | --- |
| 22 | SSH | TCP | UNREACHABLE (banner timeout) |
| 8000 | tv-webhook (FastAPI) | TCP | Entrypoint webhook TradingView |
| 8010 | perf engine (FastAPI) | TCP | Performance tracking |
| 8080 | desk_pro (possible) | TCP | Desk Pro API |
| 51820 | WireGuard (wg0) | UDP | Hub VPN (si actif) |
| 51821 | WireGuard (wg-mgmt) | UDP | WG management (vu sur db-layer) |
| 18789 | OpenClaw (non confirme) | TCP | Non attendu sur admin-trading |
| 18790 | OpenClaw lab (non confirme) | TCP | Non attendu sur admin-trading |

## Processus attendus

### Python / uvicorn

| Processus | Script | Role |
| --- | --- | --- |
| uvicorn / python | webhook_server.py | Serveur webhook principal |
| uvicorn / python | perf/perf_app.py | Serveur performance (si actif) |

### Desk Pro (lancement manuel ou cron)

| Processus | Commande | Role |
| --- | --- | --- |
| python -m modules.desk_pro_runner | desk_pro_cmd.sh run | Orchestration Desk Pro |

### Vision / Telegram

| Processus | Script | Role |
| --- | --- | --- |
| bash | vision_bot watch | Watch loop captures |
| python | bot_vision_step2 | Analyse + envoi Telegram |

## Tmux

| Session possible | Contenu |
| --- | --- |
| desk-pro | Desk Pro runner |
| vision-bot | Vision bot watch |
| webhook | Webhook server logs |

## Etat inconnu (a verifier apres retablissement)

- Services reellement actifs vs installes mais arretes
- Ports reellement en ecoute
- Processus reellement en cours
- Tmux sessions actives
- Cron jobs configures
- .env / secrets (ne pas afficher)
