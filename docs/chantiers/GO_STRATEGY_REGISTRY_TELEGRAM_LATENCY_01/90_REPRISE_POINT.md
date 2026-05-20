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

## Résumé

- Strategy Registry étendu avec une colonne `telegram_latency`
- telemetry `sendMessage` enrichie par tags `strategy_id/version`
- backtest offline peut produire un breakdown par stratégie

## Vérif (local)

```powershell
python -m pytest tests\e2e\test_telegram_latency_backtest.py -q
python -m pytest tests\e2e\test_dispatcher.py -q
```

## Next GO bundle

```text
GO_SIGNAL_CHAIN_E2E_DRY_RUN_01
```
