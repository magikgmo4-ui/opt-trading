---
go_id: GO_OPT_TRADING_DESKPRO_ALERT_WEBHOOK_ADAPTER_01
doc_type: closeout
repo: opt-trading
status: CLOSED / MERGED
closed_at: 2026-05-18
---

# GO_OPT_TRADING_DESKPRO_ALERT_WEBHOOK_ADAPTER_01 — CLOSEOUT

## 7_CANONICAL_STATE

```text
WEBHOOK_ADAPTER = CLOSED / MERGED
UNITTEST = 111_PASS
TELEGRAM_DELIVERY = DELIVERED
WEBHOOK_GENERIC_DELIVERY = DELIVERED (local receiver + body_keys confirmed)
WEBHOOK_TELEGRAM_API_URL = FAILED_EXPLICIT (no HTTP call, clear reason)
SECRETS = NOT_IN_GIT
```

## 13_ESTABLISHED

| Élément | État |
|---|---|
| Patch `_webhook_send` | `api.telegram.org` → reason explicite, pas d'appel HTTP |
| `TestWebhookSendAdapter` | 4 nouveaux tests PASS |
| `telegram: delivered` | confirmé (TELEGRAM_BOT_TOKEN natif) |
| `webhook: delivered` | confirmé (receiver local, body `{ts,status,message}`) |
| Telegram API URL → reason | `webhook_url_is_telegram_api — use TELEGRAM_BOT_TOKEN for Telegram` |
| ngrok | tunnel existant port 8010 (plan gratuit, 1 tunnel simultané) |
| Tests | 111/111 PASS |
| Secrets | `.env` gitignored, non commité |

## Règle de séparation documentée

```
TELEGRAM_BOT_TOKEN + TELEGRAM_CHAT_ID  →  chemin Telegram natif (_telegram_send)
ALERT_WEBHOOK_URL                       →  webhook générique JSON uniquement
                                           (NE PAS pointer vers api.telegram.org)
```

## Smoke runtime — 2026-05-18T18:15:xx

```
telegram : delivered | reason: telegram
webhook  : delivered | reason: webhook status=200

receiver events:
  path=/hook  body_keys=[ts, status, message]  len=117
```

Aucun token ni URL sensible dans les logs ou réponses.
