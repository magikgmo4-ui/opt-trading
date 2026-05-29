---
doc_id: GO_OPT_TRADING_TELEGRAM_INGESTION_CHILD_MESSAGE_NORMALIZER_01_INBOX
doc_type: inbox
repo: opt-trading
go_id: GO_OPT_TRADING_TELEGRAM_INGESTION_CHILD_MESSAGE_NORMALIZER_01
status: open
created_at: 2026-05-29
updated_at: 2026-05-29
---

# GO_OPT_TRADING_TELEGRAM_INGESTION_CHILD_MESSAGE_NORMALIZER_01

## Rôle

Child GO d'implémentation du normalizer de messages Telegram inbound,
rattaché à `GO_OPT_TRADING_TELEGRAM_INGESTION_PARENT_OPEN_01`.

Prend RawMessage de l'inbound parser, détecte le type (text/link/poll/image),
extrait métadonnées (mentions, hashtags, URLs), produit InboundMessage normalisé.

## Prochain geste

```text
GO_OPT_TRADING_TELEGRAM_INGESTION_CHILD_MESSAGE_NORMALIZER_01
```
