---
doc_id: GO_PERF_ENGINE_STRATEGY_SCORE_01_REPRISE_POINT
doc_type: reprise_point
repo: opt-trading
go_id: GO_PERF_ENGINE_STRATEGY_SCORE_01
status: active
source_kind: canonical
updated_at: 2026-05-19
---

# 90_REPRISE_POINT - GO_PERF_ENGINE_STRATEGY_SCORE_01

## MASTER_TARGET

Ce child reste subordonne au parent umbrella
`GO_OPT_TRADING_ADMIN_TRADING_SIGNAL_CHAIN_TOTAL_PRODUCT_PARENT_01` et a son
produit final total voulu :

- runtime operateur distant
- TradingView/webhook -> signal_event -> Desk Pro -> Telegram/Sheets/Perf
- Bot Vision / headless screener -> Desk Pro -> Perf
- Telegram inbound screener -> claims -> Desk Pro -> Perf
- Telegram outbound notification multi-destinations
- Google Sheets global
- Strategy Registry / Perf Engine / replay / paper

## Résumé

- schéma d’input (Observation Events) cadré
- métriques + gates V1 définies (paramétrables)
- evidence pack JSON stable défini
- scorer implémenté en CLI (fixtures-first)

## Validation locale

Commande executee dans cette passe :

```powershell
python -m pytest tests\e2e\test_perf_engine_strategy_score.py -q
```

Resultat :

```text
1 passed in 0.25s
```

## Vérif (local)

```powershell
python -m pytest tests\e2e\test_perf_engine_strategy_score.py -q
```

## Next GO bundle

```text
GO_STRATEGY_REGISTRY_TELEGRAM_LATENCY_01
```

## Tableau Kanban du bundle

Le tableau Kanban du bundle reste la navigation principale. Ce point de reprise
sert seulement a transmettre l'etat local du scoring strategie Perf Engine dans
la chaine du produit final total.

## Prochain item Kanban exact

`GO_STRATEGY_REGISTRY_TELEGRAM_LATENCY_01`

## Gaps encore ouverts

- producer officiel ObservationEvent encore absent
- consumer officiel registry ou Trading Lab encore absent
- export Sheets `strategy_perf` encore hors scope
- metrics avancees du parent encore non branchees dans ce V1
