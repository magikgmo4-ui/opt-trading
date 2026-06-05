---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_PARENT_REVIEW_01_SURFACE_MAP
doc_type: surface_cartography
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_PARENT_REVIEW_01
status: active
surface: chantier
source_kind: canonical
updated_at: 2026-05-04
---

# 30_TRADING_SURFACE_MAP — admin-trading

Cartographie des surfaces trading deduites des registres et du repo. Etat runtime non verifiable (machine unreachable).

## 1. Webhook / Ingress

### tv-webhook (P0 critique)

| Champ | Valeur |
| --- | --- |
| Entrypoint | webhook_server.py (FastAPI) |
| Port attendu | 8000 |
| Auth | HMAC (modules.auth.webhook_key) |
| Flux | TradingView alert -> webhook -> risk -> execution -> position -> perf |
| Telegram | Alertes via Telegram Bot API |
| Systemd | tv-webhook.service |
| Ngrok | ngrok-tv.service (tunnel TradingView) |

### Modules associes

| Module | Role |
| --- | --- |
| modules/webhook/ | Normalisation payload webhook |
| modules/auth/webhook_key.py | Validation HMAC |
| modules/risk_engine/ | Calcul risque live |
| modules/execution_engine/ | Execution trades |
| modules/position_engine/ | Gestion positions |

## 2. Desk Pro (P0 critique)

### desk_pro_runner

| Champ | Valeur |
| --- | --- |
| Module | modules/desk_pro_runner |
| Script | scripts/admin_trading/desk_pro_cmd.sh |
| Machine cible | admin_trading |
| Role | Orchestration principale trading |
| Dependances | probability_engine, decision_engine |
| Sorties | /shared/desk_pro/latest/ (JSON, HTML) |
| Journal | data/logs/desk_pro/session_journal.log |

### Sous-modules Desk Pro

| Module | Machine | Role |
| --- | --- | --- |
| desk_pro_dashboard | msi_db_layer | Supervision temps reel (UI) |
| desk_pro_runner | admin_trading | Orchestration backend |
| desk_analyze | admin_trading | Analyse a la demande |
| desk_capture_inputs | admin_trading | Saisie manuelle signaux |
| desk_snapshot_ingest | admin_trading | Ingestion snapshots |
| desk_retention | admin_trading | Retention donnees |

## 3. Trading Engines Chain

Pipeline de decision trading sur admin-trading :

```
collectors -> derivatives_analyzer -> probability_engine -> decision_engine
                                                              |
                              risk_engine <------------------+
                                                              |
                              position_engine -> portfolio_engine
```

### Engines

| Module | Machine | Statut registre | Priorite |
| --- | --- | --- | --- |
| probability_engine | admin_trading | active | high |
| decision_engine | admin_trading | active | high |
| risk_engine | admin_trading | active | high |
| position_engine | admin_trading | active | medium |
| portfolio_engine | admin_trading | active | medium |

## 4. Analysis Pipeline

| Module | Machine | Role | Priorite |
| --- | --- | --- | --- |
| derivatives_analyzer | admin_trading | Analyse marches derives | high |
| liquidation_analyzer | admin_trading | Niveaux liquidation | medium |
| market_scanner | admin_trading | Scanner marche | medium |
| opportunity_ranker | admin_trading | Classement opportunites | medium |

## 5. Collectors

| Module | Machine | Role |
| --- | --- | --- |
| derivatives_collector | admin_trading | Collecte donnees derives |
| packages/collectors_core | admin_trading | Aides runtime partagees |

## 6. Vision / ShareX / Telegram

### Pipeline Vision

```
ShareX (Windows/cursor-ai) -> SFTP -> vision_inbox
     -> vision_bot (watch loop) -> vision_outbox (.md)
     -> bot_vision_step2 (analyse) -> Telegram

Bot Vision Headless (Playwright/Chromium):
     -> capture_headless.js (timer 10min) -> vision_inbox (PNG + JSON)
     -> vision_bot -> vision_processed -> vision_outbox
     -> desk_bridge (guarded) -> desk/snapshots
```

### Modules

| Module | Machine | Role |
| --- | --- | --- |
| vision_bot | admin_trading | Capture inbox -> outbox via OCR |
| bot_vision_step2 | admin_trading | Analyse Vision + Telegram |
| bot_vision_headless | admin_trading | Capture headless Playwright/Chromium (timer 10min) |
| shared_files_sftp | admin_trading | Serveur SFTP /shared |

## 7. Perf / Monitoring

| Module | Machine | Role |
| --- | --- | --- |
| perf_engine | admin_trading | Collecte metriques performance |
| perf/perf_app.py | admin_trading | FastAPI + Desk Pro mount |
| Telegram alerts | admin_trading | No-activity / drawdown alerts |

## 8. Network / Infrastructure

| Composant | Role |
| --- | --- |
| WireGuard (wg0) | Hub VPN — 10.66.66.1 |
| WireGuard (wg-mgmt) | Management VPN |
| SSH | ghost@192.168.0.111:22 |
| shared_files_sftp | Serveur SFTP /shared |
| scripts/admin_trading/ | Couche integration machine |

## 9. UI Surfaces (referencees dans les registres)

Toutes les surfaces ci-dessous sont referencees dans `registry/ui_surfaces_registry.yaml` avec `machine_target: admin_trading` :

| Surface | Module | Actions |
| --- | --- | --- |
| desk_pro_runner | desk_pro_runner | cmd-desk_pro_runner run |
| desk_analyze | desk_analyze | cmd-desk_analyze |
| desk_capture_inputs | desk_capture_inputs | cmd-desk_capture_inputs |
| desk_snapshot_ingest | desk_snapshot_ingest | cmd-desk_snapshot_ingest |
| desk_retention | desk_retention | cmd-desk_retention clean |
| desk_state | desk_pro_dashboard | cmd-desk_state |
| bot_vision | vision_bot | cmd-bot_vision capture |
| probability_engine | probability_engine | cmd-probability_engine sample |
| decision_engine | decision_engine | cmd-decision_engine evaluate |
| risk_engine | risk_engine | cmd-risk_engine check |
| portfolio_engine | portfolio_engine | cmd-portfolio_engine sync |
| position_engine | position_engine | cmd-position_engine monitor |
| derivatives_analyzer | derivatives_analyzer | cmd-derivatives_analyzer analyze |
| liquidation_analyzer | liquidation_analyzer | cmd-liquidation_analyzer scan |
| market_scanner | market_scanner | cmd-market_scanner run |
| opportunity_ranker | opportunity_ranker | cmd-opportunity_ranker rank |
| perf_engine | perf_engine | cmd-perf_engine measure |

## RISKS

- À qualifier.
