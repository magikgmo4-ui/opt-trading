---
doc_id: GO_OPT_TRADING_DATA_CENTER_CHILD_ACCEPTANCE_CLOSE_GATE_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
project: opt-trading
module: data_center
go_id: GO_OPT_TRADING_DATA_CENTER_CHILD_ACCEPTANCE_CLOSE_GATE_01
parent_go_id: GO_OPT_TRADING_DATA_CENTER_PARENT_OPEN_01
status: open
lifecycle_stage: acceptance
surface: docs/chantiers
source_kind: canonical
created_at: 2026-05-23
updated_at: 2026-05-23
GO_STRUCTURAL_ROLE: GO_CHILD_ATTACHED_TO_PARENT
PF_ID: PF_DATA_CENTER
MASTER_PROJECT_PLAN_ID: MPP_DATA_CENTER_NORMALIZED_REGISTRY
PARENT_GO_ID: GO_OPT_TRADING_DATA_CENTER_PARENT_OPEN_01
BUNDLE_TARGET: MARKET_METRICS_CONSUMER_DECOUPLING_CLOSE_GATE
NEXT_ATTACH_TARGET: null
NEXT_GO: null
topic_keys:
  - opt-trading
  - data_center
  - acceptance
  - close_gate
  - market_metrics
  - consumer_decoupling
links:
  - docs/chantiers/GO_OPT_TRADING_DATA_CENTER_PARENT_OPEN_01/00_INITIAL_PROJECT_DOC.md
  - docs/chantiers/GO_OPT_TRADING_DATA_CENTER_CHILD_HISTORY_VIEW_MARKET_METRICS_01/90_REPRISE_POINT.md
  - modules/data_center/registry/consumers.json
  - modules/data_center/registry/producers.json
  - modules/data_center/tests/test_contract_tests.py
  - modules/derivatives_collector/app/market_metrics_writer.py
  - modules/desk_pro/service/market_metrics_reader.py
---

# GO_OPT_TRADING_DATA_CENTER_CHILD_ACCEPTANCE_CLOSE_GATE_01

## Objet

Produire le rapport d'acceptation du bloc livré :

```text
GO_OPT_TRADING_DATA_CENTER_MARKET_METRICS_CONSUMER_DECOUPLING_BLOCK_01
```

Ce bloc couvre : la règle `producer <> view <> consumer` pour `market_metrics.v1`, les 3 access patterns, le registry, les writers, et la migration Desk Pro.

## Périmètre du close gate

| Fermé | Objet |
|---|---|
| **OUI** | Bloc `MARKET_METRICS_CONSUMER_DECOUPLING_BLOCK_01` |
| NON | `PF_DATA_CENTER` |
| NON | `GO_OPT_TRADING_DATA_CENTER_PARENT_OPEN_01` |
| NON | `MPP_DATA_CENTER_NORMALIZED_REGISTRY` |

## Bloc fermé — PRs mergées

| PR | GO | Objet |
|---|---|---|
| `#745` | `GO_OPT_TRADING_DATA_CENTER_PARENT_OPEN_01` | parent Data Center ouvert |
| `#747` | storage réconcilié | market_metrics storage aligning |
| `#749` | `CONTRACT_TESTS_01` | contract smoke tests (28 tests) |
| `#751` | `CONTRACT_CLASS_VIEW_MARKET_METRICS_01` | vue neutre market_metrics.v1 |
| `#753` | `DESKPRO_VIEW_MIGRATION_01` | Desk Pro migré vers DC view |
| `#755` | `LATEST_CONSUMERS_VIEW_MIGRATION_01` | latest_only consumers verrouillés |
| `#758` | `BY_SYMBOL_CONSUMER_VIEW_01` | by_symbol consumers verrouillés |
| `#761` | `HISTORY_VIEW_MARKET_METRICS_01` | full_history / perf_engine corrigé |

## Règle canonique établie

```text
data/data_center/<family>/<producer_id>/   → écriture producteur (source d'audit)
data/data_center/views/<contract_class>/   → lecture consumer (surface neutre)
```

## 6_FINAL_TARGET

- Rapport d'acceptation du bloc market_metrics.v1 consumer-decoupling : ACCEPTED.
- Gaps restants documentés comme NEXT_GO.
- PF_DATA_CENTER reste OPEN.

## 12_INVARIANTS

- Aucun appel API, DB, Telegram.
- Aucun reader fantôme créé.
- PF_DATA_CENTER non fermé.
- Parent GO non fermé.
- Aucune modification aux index globaux non référencés.
