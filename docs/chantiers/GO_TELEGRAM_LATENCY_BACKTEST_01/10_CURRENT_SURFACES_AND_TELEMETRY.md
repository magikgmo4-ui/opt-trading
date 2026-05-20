---
doc_id: GO_TELEGRAM_LATENCY_BACKTEST_01_CURRENT_SURFACES_AND_TELEMETRY
doc_type: inventory
repo: opt-trading
go_id: GO_TELEGRAM_LATENCY_BACKTEST_01
status: reference
source_kind: canonical
updated_at: 2026-05-19
---

# 10_CURRENT_SURFACES_AND_TELEMETRY - État actuel

## Surfaces outbound Telegram

| Surface | Preuve | API | Notes |
| --- | --- | --- | --- |
| Notification dispatcher | `modules/notification_dispatcher/app/dispatcher.py` | Bot API sendMessage | routage par event_type |
| Webhook TradingView | `modules/webhook_server/webhook_server.py` | Bot API sendMessage | messages test/real |
| Desk Pro alerts | `modules/desk_pro_alerts/*` | Bot API sendMessage | alert test endpoint |
| Helper shared | `shared/telegram_notify.py` | Bot API sendMessage | wrapper unique |

## Telemetry (latence)

La telemetry est maintenant enregistrée en JSONL:

- path par défaut: `data/telemetry/telegram_send.jsonl`
- override: `TELEGRAM_LATENCY_LOG_PATH`

Chaque envoi écrit un record:

- `timestamp` (UTC ISO)
- `source` (caller label)
- `ok` (bool)
- `duration_ms` (int)
- `status_code` (int|null)
- `timeout_s` (float)
- `message_len` (int)
- `error` (str|null)

## Outil offline

Backtest analyzer:

- `scripts/telegram/latency_backtest.py`

## Validation locale executee

Commande relancee dans cette passe :

```powershell
python -m pytest tests\e2e\test_telegram_latency_backtest.py -q
```

Resultat observe :

```text
1 passed
```

## Ancrage umbrella

- `MASTER_TARGET` : contribuer au produit final total via la mesure de latence Telegram outbound
- `Kanban bundle` : reste la reference principale
- `Prochain item Kanban` : `GO_PERF_ENGINE_STRATEGY_SCORE_01`
- `Gaps encore ouverts` : pas de true e2e reception client, pas de retry policy commune, pas de raccord perf/registry
