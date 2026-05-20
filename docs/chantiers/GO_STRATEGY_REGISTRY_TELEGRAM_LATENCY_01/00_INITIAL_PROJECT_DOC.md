---
doc_id: GO_STRATEGY_REGISTRY_TELEGRAM_LATENCY_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
go_id: GO_STRATEGY_REGISTRY_TELEGRAM_LATENCY_01
status: active
lifecycle_stage: cadrage
source_kind: canonical
updated_at: 2026-05-19
links:
  - docs/chantiers/GO_STRATEGY_CANONICAL_FRAMEWORK_PARENT_01/95_STRATEGY_REGISTRY.md
  - docs/chantiers/GO_TELEGRAM_LATENCY_BACKTEST_01/90_REPRISE_POINT.md
  - docs/chantiers/GO_PERF_ENGINE_STRATEGY_SCORE_01/90_REPRISE_POINT.md
  - docs/chantiers/GO_STRATEGY_REGISTRY_TELEGRAM_LATENCY_01/10_CURRENT_REGISTRY_SURFACES.md
  - docs/chantiers/GO_STRATEGY_REGISTRY_TELEGRAM_LATENCY_01/20_REGISTRY_FIELD_UPDATE.md
  - docs/chantiers/GO_STRATEGY_REGISTRY_TELEGRAM_LATENCY_01/30_VALIDATION_FLOW.md
  - docs/chantiers/GO_STRATEGY_REGISTRY_TELEGRAM_LATENCY_01/40_GAPS_AND_NEXT_GO.md
  - docs/chantiers/GO_STRATEGY_REGISTRY_TELEGRAM_LATENCY_01/90_REPRISE_POINT.md
---

# 00_INITIAL_PROJECT_DOC - Strategy Registry: telegram_latency

## But

Étendre le Strategy Registry avec une dimension `telegram_latency` qui:

- est mesurable offline (telemetry JSONL)
- peut être rattachée à une stratégie (tags: strategy_id/version)
- alimente les gates (promotion/retirement) sans décision live

## Contraintes

- pas de secrets, pas de chat_id/token dans le repo
- pas de listener inbound Telegram (pas getUpdates)
- pas d’impact runtime trading (instrumentation safe)

## Livrables

- champ registry `telegram_latency_status` + evidence refs
- tagging strategy_id/version dans la telemetry `sendMessage`
