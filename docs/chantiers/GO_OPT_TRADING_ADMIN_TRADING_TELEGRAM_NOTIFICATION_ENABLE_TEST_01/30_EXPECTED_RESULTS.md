---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_TELEGRAM_NOTIFICATION_ENABLE_TEST_01_30_RESULTS
doc_type: chantier/expected_results
repo: opt-trading
branch: go/GO_OPT_TRADING_ADMIN_TRADING_TELEGRAM_NOTIFICATION_ENABLE_TEST_01
machine: admin-trading
status: active
lifecycle_stage: telegram_enable_test
links:
  - docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_TELEGRAM_NOTIFICATION_ENABLE_TEST_01/20_SAFE_PAYLOAD_TEST.md
---

# 30_EXPECTED_RESULTS — Resultats attendus

## Tableau de resultats

| # | Test | HTTP | Telegram | No-trade |
| --- | --- | --- | --- | --- |
| 1 | BUY TV_TEST | 200 | Message recu | Confirme |
| 2 | SELL TV_TEST | 200 | Message recu | Confirme |
| 3 | Rejeu #1 | 200 | Message recu | Confirme |
| 4 | Rejeu #2 | 200 | Message recu | Confirme |
| 5 | Rejeu #3 | 200 | Message recu | Confirme |
| 6 | Signal INVALID | 400 | Aucun message | Confirme |
| 7 | getMe Telegram | 200 (`ok:true`) | Bot joignable | N/A |

## Criteres PASS

- Tous les payloads valides retournent `200 {"ok": true}`
- Chaque payload valide genere EXACTEMENT un message Telegram
- Les messages Telegram contiennent le format attendu (engine, signal, symbol, reason)
- Aucun message Telegram pour les payloads invalides
- Aucun trade dans le perf ledger
- `trade_allowed=false` et `admin_trading_runtime=false` inchanges
- Aucun token/secret visible dans le message Telegram
- Aucune erreur 5xx dans les logs

## Criteres FAIL

- Payload valide retourne autre chose que `200 {"ok": true}`
- Message Telegram non recu (timeout > 30s)
- Message Telegram recu pour un payload invalide
- Token ou chat ID visible dans le message Telegram
- Apparition d'un trade dans le perf ledger
- Erreur 5xx dans les logs
- `trade_allowed` ou `admin_trading_runtime` modifies

## Template de preuve Telegram

| Champ attendu | Exemple |
| --- | --- |
| Signal + Symbol + TF | `BUY TEST/USDT 1m` |
| Engine | `engine: TV_TEST` |
| Price / TP / SL | `price: 100.0 | tp: 110.0 | sl: 95.0` |
| Reason | `reason: GO_TELEGRAM_NOTIFY_TEST_01` |
| Qty / Risk | `qty: 20.0 | risk_usd: 100.0` |
| Pas de token | -- |
| Pas de chat_id | -- |

## RISKS

- À qualifier.
