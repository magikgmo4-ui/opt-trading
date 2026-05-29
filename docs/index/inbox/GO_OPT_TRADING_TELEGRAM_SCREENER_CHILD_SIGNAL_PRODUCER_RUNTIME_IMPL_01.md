---
doc_id: GO_OPT_TRADING_TELEGRAM_SCREENER_CHILD_SIGNAL_PRODUCER_RUNTIME_IMPL_01_INBOX
doc_type: inbox
repo: opt-trading
go_id: GO_OPT_TRADING_TELEGRAM_SCREENER_CHILD_SIGNAL_PRODUCER_RUNTIME_IMPL_01
status: open
created_at: 2026-05-28
updated_at: 2026-05-28
---

# GO_OPT_TRADING_TELEGRAM_SCREENER_CHILD_SIGNAL_PRODUCER_RUNTIME_IMPL_01

## Rôle

Child GO de production de signaux Telegram Screener normalisés + adaptation
Desk Pro, rattaché à `GO_OPT_TRADING_TELEGRAM_SCREENER_PARENT_OPEN_01`.

Transforme les `ScreenerSignal` du parser en `ScreenerProducedSignal` puis
en `telegram_claim.v1` pour Desk Pro.

## État

- Signal producer implémenté dans `modules/telegram_screener/signal/`
- Desk Pro adapter compatible telegram_claim.v1
- 18 tests validés

## Prochain geste

```text
GO_OPT_TRADING_TELEGRAM_SCREENER_PARENT_OPEN_01
```
