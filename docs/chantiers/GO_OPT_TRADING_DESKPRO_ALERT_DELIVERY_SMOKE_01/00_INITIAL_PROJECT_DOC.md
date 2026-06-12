---
go_id: GO_OPT_TRADING_DESKPRO_ALERT_DELIVERY_SMOKE_01
doc_type: initial_project_doc
repo: opt-trading
status: DRAFT
created_at: 2026-05-18
---

# GO_OPT_TRADING_DESKPRO_ALERT_DELIVERY_SMOKE_01

## 1_MASTER_TARGET

Permettre de tester manuellement la livraison d'alerte vers les destinations configurées (Telegram, webhook), sans attendre un état degraded/down, avec statut returned.

## 10_IMPLEMENTATION

### routes.py

- `POST /desk/alert/test` → déclenche une alerte de test
  - Lit les destinations depuis env
  - Appelle _dispatch_alert avec un payload de test
  - Retourne le statut par destination (delivered/skipped/failed)
  - Ne modifie pas _alert_state (pas de cooldown sur le test)
  - Aucun secret loggé

### page.py

- Ajouter un bouton "Test Alert" dans la Pipeline Status card
- Affiche le résultat (✓ / ✗) par destination

## 13_ESTABLISHED

- `_dispatch_alert()` existe (PR #554)
- `_telegram_send()`, `_webhook_send()` existent
- 322/322 PASS

## RISKS

- À qualifier.
