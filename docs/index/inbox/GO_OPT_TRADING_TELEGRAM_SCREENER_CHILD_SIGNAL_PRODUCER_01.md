---
doc_id: GO_OPT_TRADING_TELEGRAM_SCREENER_CHILD_SIGNAL_PRODUCER_01_INBOX
doc_type: inbox
repo: opt-trading
go_id: GO_OPT_TRADING_TELEGRAM_SCREENER_CHILD_SIGNAL_PRODUCER_01
status: open
created_at: 2026-05-28
updated_at: 2026-05-28
---

# GO_OPT_TRADING_TELEGRAM_SCREENER_CHILD_SIGNAL_PRODUCER_01 — inbox

## Rôle

Child GO de production de screener signals normalisés vers Desk Pro,
rattaché à `GO_OPT_TRADING_TELEGRAM_SCREENER_PARENT_OPEN_01`.

## État

- Signal spec défini.
- Prochaine étape : implémenter le signal producer + adapter Desk Pro.

## Prochain geste

Implémenter le signal producer dans `modules/telegram_screener/signal/`.
