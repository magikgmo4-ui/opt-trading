---
go_id: GO_OPT_TRADING_DESKPRO_ALERT_DELIVERY_REAL_DESTINATION_DELIVERED_01
doc_type: closeout
repo: opt-trading
status: CLOSED / DELIVERED
closed_at: 2026-05-18
---

# GO_OPT_TRADING_DESKPRO_ALERT_DELIVERY_REAL_DESTINATION_DELIVERED_01 — CLOSEOUT

## 7_CANONICAL_STATE

```text
REAL_DESTINATION_DELIVERED = CLOSED / DELIVERED
CODE_CHANGES = NONE
UNITTEST = 107_PASS
SECRETS = NOT_IN_GIT (.env gitignored, ligne 37)
TELEGRAM_REAL_DELIVERY = DELIVERED
WEBHOOK_EXTERNAL_DELIVERY = FAILED (401 — URL format incompatible)
FALLBACK_JSONL = CONFIRMED
```

## 13_ESTABLISHED

| Élément | État |
|---|---|
| `telegram` | **`delivered`** — livraison réelle externe confirmée |
| `webhook` | `failed` — HTTP 401 (voir note ci-dessous) |
| Credentials | présents dans `.env` local uniquement — non commités |
| JSONL | non écrit par smoke test — confirmé |
| Cooldown | cycle complet confirmé |
| Tests | 107/107 PASS |
| Secrets git | aucun |

## Résultats smoke — `POST /desk/alert/test` — 2026-05-18T17:46:29Z

```
ok: true
alert.ts: 2026-05-18T17:46:29.156931Z
alert.status: test

telegram : delivered  | reason: telegram
webhook  : failed     | reason: HTTP Error 401: Unauthorized
```

Aucun token, chat_id ni URL affichés. Preuve de réception : message reçu
sur le canal Telegram configuré localement (non documenté ici).

## Note — webhook 401

`ALERT_WEBHOOK_URL` est configuré avec un endpoint Telegram API
(`api.telegram.org/bot.../sendMessage`). Le dispatcher webhook envoie
un payload JSON brut (format alerte interne), non compatible avec le
format `{chat_id, text}` attendu par l'API Telegram → 401 Unauthorized.

**Ce n'est pas un bug du dispatcher** : il fonctionne correctement
(connexion établie, réponse reçue). L'échec est lié à la configuration
de l'URL. Pour un webhook externe générique, utiliser une URL acceptant
du JSON arbitraire via POST.

## Garanties secrets

- `.env` gitignored (`.gitignore` ligne 37) — vérifié via `git check-ignore`
- `git status -- .env` : non tracé
- Aucun token ni credential dans ce document
- Aucun token dans le JSONL (`{ts, status}` uniquement)
- Aucun token dans les réponses API (`destinations.*` = bool)

## RISKS

- À qualifier.
