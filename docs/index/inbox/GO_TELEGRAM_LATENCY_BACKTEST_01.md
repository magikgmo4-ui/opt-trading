---
doc_id: GO_TELEGRAM_LATENCY_BACKTEST_01_INBOX
repo: opt-trading
project: opt-trading
go_id: GO_TELEGRAM_LATENCY_BACKTEST_01
status: open
surface: index_inbox
source_kind: canonical
updated_at: 2026-05-19
topic_keys:
  - telegram
  - latency
  - backtest
  - telemetry
  - signal_chain
links:
  - docs/chantiers/GO_TELEGRAM_LATENCY_BACKTEST_01/00_INITIAL_PROJECT_DOC.md
  - docs/chantiers/GO_TELEGRAM_LATENCY_BACKTEST_01/10_CURRENT_SURFACES_AND_TELEMETRY.md
  - docs/chantiers/GO_TELEGRAM_LATENCY_BACKTEST_01/20_METHODOLOGY_AND_METRICS.md
  - docs/chantiers/GO_TELEGRAM_LATENCY_BACKTEST_01/30_BACKTEST_OUTPUT_SCHEMA.md
  - docs/chantiers/GO_TELEGRAM_LATENCY_BACKTEST_01/40_GAPS_AND_NEXT_GO.md
  - docs/chantiers/GO_TELEGRAM_LATENCY_BACKTEST_01/90_REPRISE_POINT.md
---

# INBOX - GO_TELEGRAM_LATENCY_BACKTEST_01

## Objet

Mettre en place un backtest “latency Telegram” basé sur des logs telemetry, sans dépendre d’un bot inbound live (fixtures-first). L’objectif est de mesurer et comparer la latence d’envoi (sendMessage) par surface (dispatcher, webhook, desk alerts, etc.).

## Point de reprise

```text
docs/chantiers/GO_TELEGRAM_LATENCY_BACKTEST_01/20_METHODOLOGY_AND_METRICS.md
docs/chantiers/GO_TELEGRAM_LATENCY_BACKTEST_01/30_BACKTEST_OUTPUT_SCHEMA.md
docs/chantiers/GO_TELEGRAM_LATENCY_BACKTEST_01/40_GAPS_AND_NEXT_GO.md
```
