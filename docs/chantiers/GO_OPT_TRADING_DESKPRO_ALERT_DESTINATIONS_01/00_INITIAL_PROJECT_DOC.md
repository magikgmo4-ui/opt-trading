---
go_id: GO_OPT_TRADING_DESKPRO_ALERT_DESTINATIONS_01
doc_type: initial_project_doc
repo: opt-trading
status: DRAFT
created_at: 2026-05-18
---

# GO_OPT_TRADING_DESKPRO_ALERT_DESTINATIONS_01

## 1_MASTER_TARGET

Brancher des destinations d'alerte optionnelles (Telegram, webhook) au-dessus du dispatch Desk Pro (PR #552), avec fallback JSONL/local et aucun secret en code.

## 10_IMPLEMENTATION

### routes.py

- `_TELEGRAM_BOT_TOKEN`, `_TELEGRAM_CHAT_ID`, `_ALERT_WEBHOOK_URL` lues depuis env
- `_telegram_send(text)` → POST Telegram API si configuré
- `_webhook_send(alert)` → POST URL si configurée
- `_dispatch_alert(alert)` → appelle les deux, retourne résultats
- `_check_alert` → `dispatch` field dans la réponse triggered
- `/desk/alerts` → `destinations` field montrant ce qui est configuré

### page.py

- Dispatch status (✓ telegram, ✗ webhook) dans la barre d'alerte orange

## 13_ESTABLISHED

- Alert dispatch existant (PR #552)
- 322/322 PASS
- Aucun secret en code, uniquement env vars
