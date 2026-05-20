---
doc_id: GO_TELEGRAM_LATENCY_BACKTEST_01_METHODOLOGY_AND_METRICS
doc_type: methodology
repo: opt-trading
go_id: GO_TELEGRAM_LATENCY_BACKTEST_01
status: active
source_kind: canonical
updated_at: 2026-05-19
---

# 20_METHODOLOGY_AND_METRICS

## Définition de la latence mesurée

Dans ce GO, “latence Telegram” = durée du call HTTP `sendMessage` côté producer:

```text
t_start = avant requests.post()
t_end   = après réponse HTTP (ou exception)
duration_ms = t_end - t_start
```

Ce n’est pas la latence “réception côté client Telegram”, mais c’est un proxy exploitable pour:

- comparer les surfaces entre elles
- détecter des dégradations (p95/p99)
- calibrer des timeouts et des retry policies

## Backtest offline (fixtures-first)

1) générer/accumuler `telegram_send.jsonl` via les runs dry-run / alert tests / dispatcher tests

2) analyser:

```powershell
python scripts\telegram\latency_backtest.py
python scripts\telegram\latency_backtest.py --since 2026-05-19T00:00:00+00:00
```

## Métriques cibles

- `ok_rate`
- `p50_ms`, `p90_ms`, `p95_ms`, `p99_ms`, `max_ms`
- breakdown par `source`

## Règles de lecture

- si `ok_rate < 0.99` sur une surface critique: considérer la surface “unstable”
- si `p95_ms` explose: éviter “reaction strategies” temps-réel, privilégier paper/replay

## Ancrage umbrella

- `MASTER_TARGET` : cadrer la latency Telegram du produit final total sans melanger inbound et outbound
- `Tableau Kanban du bundle` : reste la navigation principale
- `Produit final total voulu` : chaines separees mais liees entre webhook, Desk Pro, Telegram, Sheets, Perf et runtime
- `Prochain item Kanban exact` : `GO_PERF_ENGINE_STRATEGY_SCORE_01`
- `Gaps encore ouverts` : calibration retry/timeout par tier, seuils de gating perf non relies, pas de mesure client-side
