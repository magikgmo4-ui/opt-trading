---
doc_id: GO_STRATEGY_REGISTRY_TELEGRAM_LATENCY_01_CURRENT_REGISTRY_SURFACES
doc_type: inventory
repo: opt-trading
go_id: GO_STRATEGY_REGISTRY_TELEGRAM_LATENCY_01
status: reference
source_kind: canonical
updated_at: 2026-05-19
---

# 10_CURRENT_REGISTRY_SURFACES - État actuel

## Strategy registry (source canonique)

- source: `docs/chantiers/GO_STRATEGY_CANONICAL_FRAMEWORK_PARENT_01/95_STRATEGY_REGISTRY.md`
- loader: `modules/strategy/registry.py`
- validation: `modules/strategy/adapter.py` + `tools/strategy/validate_strategy_registry.py`

## Telegram latency (telemetry + backtest)

- telemetry `sendMessage` JSONL: `shared/telegram_notify.py` (duration_ms, ok, source)
- backtest offline: `scripts/telegram/latency_backtest.py`

## Gap

La telemetry existante est agrégée par `source` (caller). Pour rattacher une latence à une stratégie, il faut des tags (`strategy_id`, `strategy_version`) dans la telemetry.
