---
doc_id: GO_OPT_TRADING_TELEGRAM_INGESTION_CHILD_CONSUMER_DISTRIBUTION_01_INBOX
doc_type: inbox
repo: opt-trading
go_id: GO_OPT_TRADING_TELEGRAM_INGESTION_CHILD_CONSUMER_DISTRIBUTION_01
status: open
created_at: 2026-05-29
updated_at: 2026-05-29
---

# GO_OPT_TRADING_TELEGRAM_INGESTION_CHILD_CONSUMER_DISTRIBUTION_01

## Rôle

Child GO d'implémentation de la distribution des messages normalisés,
rattaché à `GO_OPT_TRADING_TELEGRAM_INGESTION_PARENT_OPEN_01`.

Prend InboundMessage du normalizer, route vers consumers par canal
(Screener, Desk Pro, Data Center).

## Prochain geste

```text
GO_OPT_TRADING_TELEGRAM_INGESTION_CHILD_CONSUMER_DISTRIBUTION_01
```
