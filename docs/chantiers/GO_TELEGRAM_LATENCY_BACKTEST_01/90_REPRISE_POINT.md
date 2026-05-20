---
doc_id: GO_TELEGRAM_LATENCY_BACKTEST_01_REPRISE_POINT
doc_type: reprise_point
repo: opt-trading
go_id: GO_TELEGRAM_LATENCY_BACKTEST_01
status: active
source_kind: canonical
updated_at: 2026-05-19
---

# 90_REPRISE_POINT - GO_TELEGRAM_LATENCY_BACKTEST_01

## MASTER_TARGET

Ce child reste subordonne au parent umbrella
`GO_OPT_TRADING_ADMIN_TRADING_SIGNAL_CHAIN_TOTAL_PRODUCT_PARENT_01` et a son
produit final total voulu :

- runtime operateur distant
- TradingView/webhook -> signal_event -> Desk Pro -> Telegram/Sheets/Perf
- Bot Vision / headless screener
- Telegram inbound screener
- Telegram outbound notification multi-destinations
- Google Sheets global
- Strategy Registry / Perf Engine / replay / paper

## Résumé

- telemetry JSONL enregistrée à chaque sendMessage (duration_ms + ok)
- outil offline de backtest latency (agrégation + percentiles)
- surfaces taggées via `source`

## Validation locale

Commande executee dans cette passe :

```powershell
python -m pytest tests\e2e\test_telegram_latency_backtest.py -q
```

Resultat :

```text
1 passed in 0.23s
```

## Lecture minimale

1. `20_METHODOLOGY_AND_METRICS.md`
2. `30_BACKTEST_OUTPUT_SCHEMA.md`
3. `40_GAPS_AND_NEXT_GO.md`

## Vérif (local)

```powershell
python -m pytest tests\e2e\test_telegram_latency_backtest.py -q
```

## Next GO bundle

```text
GO_PERF_ENGINE_STRATEGY_SCORE_01
```

## Tableau Kanban du bundle

Le tableau Kanban du bundle reste la navigation principale. Ce point de reprise
sert seulement a transmettre l'etat local de la telemetry/backtest Telegram
dans la chaine du produit final total.

## Prochain item Kanban exact

`GO_PERF_ENGINE_STRATEGY_SCORE_01`

## Gaps encore ouverts

- pas de vraie mesure de reception client Telegram
- retry policy par tier encore absente
- metrics latency non reliees au Perf Engine / Strategy Registry
- aucun export Sheets transverse de ces metrics a ce stade
