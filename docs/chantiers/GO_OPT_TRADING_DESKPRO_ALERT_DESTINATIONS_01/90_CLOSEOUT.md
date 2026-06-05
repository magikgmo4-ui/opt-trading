---
go_id: GO_OPT_TRADING_DESKPRO_ALERT_DESTINATIONS_01
status: CLOSED
closeout_ts: 2026-05-18
---

## 13_ESTABLISHED

| Élément | État |
|---|---|
| PR `#554` | `MERGED` |
| Branche feature | `go/GO_OPT_TRADING_DESKPRO_ALERT_DESTINATIONS_01` supprimée |
| `sot/mainline` | mis à jour |
| Tests | `322/322 PASS` |
| `secrets/` | exclu |

## 7_CANONICAL_STATE

```text
DESKPRO_ALERT_DESTINATIONS = CLOSED / MERGED
PR_554 = MERGED
ALERT_DISPATCH_DESTINATIONS = SUPPORTED
  → Telegram if TELEGRAM_BOT_TOKEN + TELEGRAM_CHAT_ID set
  → Webhook if ALERT_WEBHOOK_URL set
  → JSONL fallback always active
SECRETS = NOT_INCLUDED
PIPELINE_COMPLETE = webhook → perf → /desk/status → health → alert → dispatch
UNITTEST = 322_PASS
```

## Livré

| Changement | Fichier |
|---|---|
| `_env_str()` lit env au dispatch time | `routes.py` |
| `_telegram_send()` POST Telegram API | `routes.py` |
| `_webhook_send()` POST webhook URL | `routes.py` |
| `_dispatch_alert()` → results list | `routes.py` |
| `/desk/status` → `alert.dispatch` | `routes.py` |
| `/desk/alerts` → `destinations` config status | `routes.py` |
| UI alert bar : ✓/✗ per destination | `page.py` |

## Prochain GO

```text
GO_OPT_TRADING_DESKPRO_ALERT_DELIVERY_SMOKE_01
```

Tester livraison réelle Telegram/webhook avec env local, sans secret commité.

## RISKS

- À qualifier.
