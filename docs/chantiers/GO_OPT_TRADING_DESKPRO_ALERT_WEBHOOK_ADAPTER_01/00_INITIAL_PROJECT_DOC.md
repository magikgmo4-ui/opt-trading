---
go_id: GO_OPT_TRADING_DESKPRO_ALERT_WEBHOOK_ADAPTER_01
doc_type: initial_project_doc
repo: opt-trading
status: CLOSED / MERGED
created_at: 2026-05-18
---

# GO_OPT_TRADING_DESKPRO_ALERT_WEBHOOK_ADAPTER_01

## 1_MASTER_TARGET

Corriger le dispatch webhook après FAILED_401 (PR #568) :
- `ALERT_WEBHOOK_URL` pointait vers `api.telegram.org` (format incompatible)
- Ajouter détection et reason explicite pour ce cas
- Garder Telegram natif et webhook générique séparés et fonctionnels

## 10_IMPLEMENTATION

### `modules/desk_pro/api/routes.py`

Ajout de `_TELEGRAM_API_HOST = "api.telegram.org"` et garde dans `_webhook_send` :

```python
if _TELEGRAM_API_HOST in url:
    return {"sent": False, "reason": "webhook_url_is_telegram_api — use TELEGRAM_BOT_TOKEN for Telegram"}
```

Aucun appel HTTP effectué si l'URL est une API Telegram — évite le 401.

### `tests/test_desk_pro_alert_test_endpoint.py`

4 nouveaux tests dans `TestWebhookSendAdapter` :
- Telegram API URL → `sent=False`, reason contient `telegram_api` et `TELEGRAM_BOT_TOKEN`
- Telegram API URL → aucun appel `urlopen`
- URL générique → appel HTTP, `sent=True` (status=200)
- URL absente → `not configured`

## 13_ESTABLISHED

- Telegram natif : DELIVERED (TELEGRAM_BOT_TOKEN path)
- Webhook générique : DELIVERED (127.0.0.1:9999 receiver, body_keys=[ts,status,message])
- Telegram API URL : FAILED — reason explicite, sans appel HTTP
- Tests : 111/111 PASS
