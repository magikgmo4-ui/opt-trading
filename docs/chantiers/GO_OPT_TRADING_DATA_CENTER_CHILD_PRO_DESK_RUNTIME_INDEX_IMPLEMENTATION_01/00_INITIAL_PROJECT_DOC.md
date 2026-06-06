---
doc_id: GO_OPT_TRADING_DATA_CENTER_CHILD_PRO_DESK_RUNTIME_INDEX_IMPLEMENTATION_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
project: opt-trading
module: data_center
go_id: GO_OPT_TRADING_DATA_CENTER_CHILD_PRO_DESK_RUNTIME_INDEX_IMPLEMENTATION_01
parent_go_id: GO_OPT_TRADING_DATA_CENTER_CHILD_PRO_DESK_RUNTIME_ACCESS_OPTIMIZATION_01
status: open
lifecycle_stage: implementation
surface: docs/chantiers
source_kind: canonical
created_at: 2026-06-06
updated_at: 2026-06-06
GO_STRUCTURAL_ROLE: GO_CHILD_ATTACHED_TO_PARENT
PF_ID: PF_DATA_CENTER
NEXT_GO: null
TRANSPORT_MODE: runtime
6_FINAL_TARGET: Implementer les compiled indexes, le registry cache, le source selector (4 modes) et le best-value resolver avec cached candidates pour market_metrics.v1. Benchmark-first, AC01-AC14 go criteria, NG01-NG08 no-go.
topic_keys:
  - opt-trading
  - data_center
  - implementation
  - compiled_indexes
  - registry_cache
  - source_selector
links:
  - docs/chantiers/GO_OPT_TRADING_DATA_CENTER_CHILD_PRO_DESK_RUNTIME_ACCESS_OPTIMIZATION_01/40_COMPILED_INDEXES_AND_CACHE_PLAN.md
  - docs/chantiers/GO_OPT_TRADING_DATA_CENTER_CHILD_PRO_DESK_RUNTIME_ACCESS_OPTIMIZATION_01/70_BENCHMARK_AND_ACCEPTANCE_CRITERIA.md
  - docs/chantiers/GO_OPT_TRADING_DATA_CENTER_CHILD_BEST_VALUE_RESOLVER_01/RESOLVER_IMPLEMENTATION_SPEC.md
  - modules/data_center/registry/pro_desk_data_inventory.json
  - modules/data_center/registry/source_candidates.json
---

# GO_OPT_TRADING_DATA_CENTER_CHILD_PRO_DESK_RUNTIME_INDEX_IMPLEMENTATION_01

## Objet

Implementer les modules runtime specifies dans le child access optimization : validation, index builder, cache, source selector, best-value resolver (cached). Benchmark-first.

## 1_MASTER_TARGET

Data Center = stockage + transit + scoring source + arbitrage source candidate. Consumer = utilise la donnee exposee.

## 6_FINAL_TARGET

```text
RUNTIME_INDEX_IMPLEMENTATION_V1
```

## 11_KEY_DECISIONS

- benchmark-first, pas resolver-first
- compiled indexes + cache = hot path
- resolver lit le cache, pas les JSON canoniques
- score=0 + candidate = not selectable
- Data Center arbitre les sources, ne decide pas les trades

## 12_INVARIANTS

- Ne pas modifier DeskPro.
- Ne pas appeler API externe depuis resolver.
- Ne pas ajouter SQLite avant benchmark.
- Ne pas publier canonical_value sans resolver_decision_ref.
