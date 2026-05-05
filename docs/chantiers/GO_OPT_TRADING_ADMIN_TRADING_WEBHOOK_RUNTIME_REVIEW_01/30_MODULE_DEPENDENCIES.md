---
doc_id: WEBHOOK_REVIEW_01_MODULES
doc_type: module_dependencies
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_WEBHOOK_RUNTIME_REVIEW_01
status: active
surface: chantier
source_kind: canonical
updated_at: 2026-05-04
---

# 30_MODULE_DEPENDENCIES

## webhook_server.py (28 KB, 788 lignes)

### Imports (runtime core)

| Module | Role | Statut |
| --- | --- | --- |
| modules.env.env | load_env(), ensure_dirs() | OK |
| shared.logger | setup_logger("tv-webhook") | OK |
| modules.risk_engine.app.risk_calculator | RiskCalculator (risk live) | actif |
| modules.execution_engine.executor | Executor (execution trades) | actif |
| modules.position_engine.position_manager | PositionManager | actif |
| modules.engines.registry | Registry engines | actif |
| modules.auth.webhook_key | payload_key_is_valid (HMAC) | actif |
| modules.desk_pro | API routes + mount | via perf_app |

### Features

| Feature | Implemente | Notes |
| --- | --- | --- |
| Webhook POST /tv | OUI | Entrypoint principal |
| HMAC auth | OUI | payload_key_is_valid |
| Risk calculator | OUI | RiskCalculator() |
| Executor | OUI | trade execution |
| Position manager | OUI | PositionManager() |
| Perf events | OUI | POST vers tv-perf:8010 |
| Telegram alerts | OUI | telegram_send() function |
| Dashboard GET /dash | OUI | HTML dashboard |
| /health endpoint | **NON** | 404 |

## perf_app.py (995 lignes)

### Features

| Feature | Implemente |
| --- | --- |
| SQLite perf.db | OUI |
| Telegram alerts (DD, no-activity) | OUI |
| Desk Pro mount | OUI (mount_desk_pro) |
| PAPER_TEST engine | OUI |
| COINM_SHORT engine | OUI |
| BITGET_SM_LITE engine | OUI |
| /perf/open | OUI |
| /perf/summary | OUI |

## Fichiers sensibles (noms seulement)

| Fichier | Contenu probable |
| --- | --- |
| /opt/trading/.env | TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, webhook keys |
| modules/auth/secrets.py | auth secrets |
| /etc/ngrok/ngrok-secrets.yml | ngrok auth token |

## Constats

- 3 engines de trading actifs (PAPER_TEST, COINM_SHORT, BITGET_SM_LITE)
- COINM_SHORT a 3507 trades fermes, 48% WR, -79K PnL
- BITGET_SM_LITE a 1051 trades, 100% WR, +210 PnL
- PAPER_TEST: 4 trades paper
- Perf events encore actifs (toutes les ~5 min)
