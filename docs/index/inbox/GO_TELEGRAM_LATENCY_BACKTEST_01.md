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

## Résultat

État établi :

- surfaces Telegram outbound et telemetry relues et reconfirmees pour `shared/telegram_notify.py`, `scripts/telegram/latency_backtest.py` et `tests/e2e/test_telegram_latency_backtest.py`
- la telemetry prouvee enregistre `timestamp`, `source`, `tags`, `ok`, `duration_ms`, `status_code`, `timeout_s`, `message_len` et `error` dans `data/telemetry/telegram_send.jsonl`
- validation relancee dans cette passe : `python -m pytest tests\e2e\test_telegram_latency_backtest.py -q` -> `1 passed`
- aucune mutation runtime introduite ; le chantier reste doc-first et offline-first

## Ancrage umbrella

- `MASTER_TARGET` : contribuer au produit final total via la mesure de latence Telegram outbound
- `Tableau Kanban du bundle` : reste la reference principale
- `Prochain item Kanban exact` : `GO_PERF_ENGINE_STRATEGY_SCORE_01`
- `Gaps encore ouverts` : pas de reception client, pas de retry policy commune, pas de raccord perf/registry

## Point de reprise

```text
docs/chantiers/GO_TELEGRAM_LATENCY_BACKTEST_01/20_METHODOLOGY_AND_METRICS.md
docs/chantiers/GO_TELEGRAM_LATENCY_BACKTEST_01/30_BACKTEST_OUTPUT_SCHEMA.md
docs/chantiers/GO_TELEGRAM_LATENCY_BACKTEST_01/40_GAPS_AND_NEXT_GO.md
```
