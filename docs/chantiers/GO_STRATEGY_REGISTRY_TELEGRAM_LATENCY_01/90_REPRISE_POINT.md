---
doc_id: GO_STRATEGY_REGISTRY_TELEGRAM_LATENCY_01_REPRISE_POINT
doc_type: reprise_point
repo: opt-trading
go_id: GO_STRATEGY_REGISTRY_TELEGRAM_LATENCY_01
status: active
source_kind: canonical
updated_at: 2026-05-19
---

# 90_REPRISE_POINT - GO_STRATEGY_REGISTRY_TELEGRAM_LATENCY_01

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

- Strategy Registry étendu avec une colonne `telegram_latency`
- telemetry `sendMessage` enrichie par tags `strategy_id/version`
- backtest offline peut produire un breakdown par stratégie

## Validation locale

Commandes executees dans cette passe :

```powershell
python -m pytest tests\e2e\test_telegram_latency_backtest.py modules\notification_dispatcher\tests\test_strategy_id_adapter_readonly.py -q
```

Resultat :

```text
8 passed in 0.66s
```

## Vérif (local)

```powershell
python -m pytest tests\e2e\test_telegram_latency_backtest.py -q
python -m pytest modules\notification_dispatcher\tests\test_strategy_id_adapter_readonly.py -q
```

## Next GO bundle

```text
GO_SIGNAL_CHAIN_E2E_DRY_RUN_01
```

## Tableau Kanban du bundle

Le tableau Kanban du bundle reste la navigation principale. Ce point de reprise
sert seulement a transmettre l'etat local du couplage registry/telegram
latency dans la chaine du produit final total.

## Prochain item Kanban exact

`GO_SIGNAL_CHAIN_E2E_DRY_RUN_01`

## Gaps encore ouverts

- tags strategy non generalises a toutes les surfaces outbound
- seuils produits de `PASS/DEGRADED/BLOCKED` non encore fixes
- evidence refs registry encore a renseigner depuis des backtests reels
- aucun export transverse vers Sheets a ce stade
