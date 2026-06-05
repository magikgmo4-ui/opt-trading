---
doc_id: GO_OPT_TRADING_DATA_CENTER_CHILD_PRO_DESK_RUNTIME_SOURCE_SELECTION_OPTIMIZATION_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
project: opt-trading
module: data_center
go_id: GO_OPT_TRADING_DATA_CENTER_CHILD_PRO_DESK_RUNTIME_SOURCE_SELECTION_OPTIMIZATION_01
parent_go_id: GO_OPT_TRADING_DATA_CENTER_PARENT_PRO_DESK_DATA_COVERAGE_01
status: open
lifecycle_stage: planning
surface: docs/chantiers
source_kind: canonical
created_at: 2026-06-05
updated_at: 2026-06-05
GO_STRUCTURAL_ROLE: GO_CHILD_ATTACHED_TO_PARENT
PF_ID: PF_DATA_CENTER
MASTER_TARGET_ID: MT_DATA_CENTER_PRO_DESK_DATA_COVERAGE
MASTER_PROJECT_PLAN_ID: MPP_DATA_CENTER_NORMALIZED_REGISTRY
PARENT_GO_ID: GO_OPT_TRADING_DATA_CENTER_PARENT_PRO_DESK_DATA_COVERAGE_01
NEXT_ATTACH_TARGET: null
6_FINAL_TARGET: Preparer l'optimisation runtime de pro_desk_data_inventory.json et source_candidates.json, maintenant en production et situes au centre producer -> Data Center -> consumer.
BUNDLE_TARGET: PRO_DESK_RUNTIME_SOURCE_SELECTION_OPTIMIZATION_V1
TRANSPORT_MODE: patch_only
CLOSE_GATE_MASTER_TARGET: not_applicable
topic_keys:
  - opt-trading
  - data_center
  - pro_desk_data
  - runtime_optimization
  - source_selection
  - compiled_indexes
  - sqlite_runtime_index
links:
  - docs/chantiers/GO_OPT_TRADING_DATA_CENTER_PARENT_PRO_DESK_DATA_COVERAGE_01/00_INITIAL_PROJECT_DOC.md
  - modules/data_center/registry/pro_desk_data_inventory.json
  - modules/data_center/registry/source_candidates.json
---

# GO_OPT_TRADING_DATA_CENTER_CHILD_PRO_DESK_RUNTIME_SOURCE_SELECTION_OPTIMIZATION_01

## 1_MASTER_TARGET

Eviter que `pro_desk_data_inventory.json` et `source_candidates.json`, maintenant en production, deviennent un goulot d'etranglement entre producers et consumers.

## 2_INITIAL_PROJECT_DOC

Ce fichier ouvre le child doc-only d'architecture runtime/source selection. Il ne modifie pas le runtime.

## 3_INITIAL_NEED

Les registres suivants sont en production :

```text
modules/data_center/registry/pro_desk_data_inventory.json
modules/data_center/registry/source_candidates.json
```

Ils sont au centre du flux :

```text
producer -> Data Center -> source selection -> views -> consumers
```

Il faut prevoir l'optimisation code/runtime/methode/langage avant la montee de charge DeskPro/Strategy/Perf/Telegram/Sheets.

## 4_MASTER_PROJECT_PLAN

1. Documenter les patterns connus multi-source / source candidate / producer-consumer.
2. Identifier les risques runtime actuels.
3. Separer cold path canonique et hot path runtime.
4. Definir les compiled indexes et le cache snapshot.
5. Verrouiller les policy profiles de source selection.
6. Evaluer SQLite runtime index en option V1.
7. Definir benchmarks et acceptance criteria.

## 6_FINAL_TARGET

```text
PRO_DESK_RUNTIME_SOURCE_SELECTION_OPTIMIZATION_V1
```

## 7_CANONICAL_STATE

Formulation verrouillee :

```text
Data Center arbitre la source.
Data Center ne decide pas l'usage.
```

Plus precis :

```text
Data Center source selector chooses the best data candidate according to an explicit policy.
Consumers decide how to use that data.
```

## 8_VALIDATED_PLAN

Livrables :

```text
10_RESEARCH_FINDINGS_MULTI_SOURCE_DATA_CENTER.md
20_CURRENT_RUNTIME_RISK_ANALYSIS.md
30_HOT_PATH_COLD_PATH_ARCHITECTURE.md
40_COMPILED_INDEXES_AND_CACHE_PLAN.md
50_SOURCE_SELECTION_POLICY_PROFILES.md
60_SQLITE_RUNTIME_INDEX_OPTION.md
70_BENCHMARK_AND_ACCEPTANCE_CRITERIA.md
90_REPRISE_POINT.md
```

## 9_SELECTED_SOLUTION

```text
JSON canonical registries
  pro_desk_data_inventory.json
  source_candidates.json

-> compile

SQLite / compiled JSON indexes
  by_data_key
  by_contract
  by_producer
  by_consumer
  by_priority

-> runtime

Data Center source selector
  scores source candidates
  preserves all candidates
  selects canonical candidate per policy
  emits resolver_decision

-> views

Data Center views
  latest
  by_symbol
  history
  all_candidates
  resolver_decisions

-> consumers

DeskPro / Strategy / Perf / Telegram / Sheets
```

## 12_INVARIANTS

- Ne pas implementer runtime dans ce child.
- Ne pas modifier les registries production dans ce child.
- Ne pas faire lire les consumers directement dans les producers raw.
- Preserver toutes les candidates.
- Ne jamais reduire source selection a un score opaque sans trace.
- Ne pas confondre source selection et decision trading.

## 16_TODO

Produire les docs du child, puis ouvrir ensuite un child implementation uniquement si les benchmarks/criteres sont valides.

## 17_RESUME_POINT

Reprendre ici : child ouvert, objectif = plan d'optimisation runtime/source selection pour les registries pro desk en production.
