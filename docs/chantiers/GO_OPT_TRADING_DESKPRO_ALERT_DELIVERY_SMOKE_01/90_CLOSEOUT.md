---
go_id: GO_OPT_TRADING_DESKPRO_ALERT_DELIVERY_SMOKE_01
doc_type: closeout
repo: opt-trading
status: CLOSED / MERGED
closed_at: 2026-05-18
pr: 557
---

# GO_OPT_TRADING_DESKPRO_ALERT_DELIVERY_SMOKE_01 — CLOSEOUT

## 7_CANONICAL_STATE

```text
DESKPRO_ALERT_DELIVERY_SMOKE = CLOSED / MERGED
PR_557 = MERGED
SOT_MAINLINE = UPDATED
UNITTEST = 107_PASS
ALERT_TEST_ENDPOINT = DELIVERED
ALERT_TEST_UI_BUTTON = DELIVERED
SECRETS = NOT_INCLUDED
```

## 13_ESTABLISHED

| Élément | État |
|---|---|
| PR `#557` | `MERGED` |
| `POST /desk/alert/test` | livré — `routes.py:262` |
| Bouton "Test Alert" | livré — `page.py:254` + handler JS `testAlert()` |
| Statut par destination | `delivered / skipped / failed` |
| `_alert_state` intact | vérifié — pas de cooldown side-effect |
| Secrets | non commités |
| Tests nouveaux | 15 |
| Suite complète | 107/107 PASS |

## 10_DELIVERED

### `POST /desk/alert/test`

- Construit un payload `{ts, status:"test", message}` sans toucher `_alert_state`
- Appelle `_dispatch_alert` existant
- Mappe `sent=True → delivered`, `reason="not configured" → skipped`, sinon `failed`
- Retourne `{ok, alert, dispatch: [{destination, status, reason}]}`

### UI — bouton "Test Alert"

- Positionné dans la Pipeline Status card
- Handler async `testAlert()` : `POST /desk/alert/test`, affiche `✓/–/✗ destination` dans le span `testAlertResult`
- `btnTestAlert` désactivé pendant la requête

### Tests — `tests/test_desk_pro_alert_test_endpoint.py`

- Sans env vars : toutes destinations `skipped`
- `sent=True` → `delivered`, `reason=not configured` → `skipped`, erreur → `failed`
- Aucun token/secret dans le payload retourné
- `_alert_state` non modifié après appel
- Exception réseau → `failed` sans raise
- Telegram + webhook avec env mocked → `delivered`

## Nuance importante

```text
Test endpoint = déclenche dispatch réel si env vars présentes
Livraison réelle externe = dépend de TELEGRAM_BOT_TOKEN / TELEGRAM_CHAT_ID / ALERT_WEBHOOK_URL
Sans env → skipped (comportement attendu en CI)
```
