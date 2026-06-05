---
doc_id: GO_OPT_TRADING_DATA_CENTER_CHILD_PRO_DESK_DATA_INVENTORY_CANONICAL_01_REGISTRY_MODEL
doc_type: registry_model
repo: opt-trading
go_id: GO_OPT_TRADING_DATA_CENTER_CHILD_PRO_DESK_DATA_INVENTORY_CANONICAL_01
status: open
source_kind: canonical
created_at: 2026-06-05
updated_at: 2026-06-05
---

# 30_REGISTRY_MODEL

## Objet

Definir le modele documentaire cible pour `pro_desk_data_inventory.json` et `pro_desk_data_fields.json` sans modifier encore les registries runtime.

## `pro_desk_data_inventory.json` — modele cible

```json
{
  "registry_version": "v1",
  "updated_at": "2026-06-05T00:00:00Z",
  "categories": [
    {
      "priority": "P10",
      "data_class": "flow_positioning",
      "role": "Positionnement, flows, open interest, liquidations, borrow et crowding.",
      "required_for": ["PF_DATA_CENTER", "PF_DESK_PRO", "PF_STRATEGY_FRAMEWORK_REGISTRY", "PF_PERF_ENGINE_TRADING_LAB"],
      "candidate_contracts": ["flow_positioning.v1", "market_metrics.v1", "liquidation_state.v1"],
      "coverage_status": "partial",
      "current_contracts": ["market_metrics.v1", "vision_context.coinglass.v1"],
      "current_gap_refs": ["G01", "G08"],
      "source_policy": "multi_source_scored",
      "freshness_target": "near_realtime_or_oneshot_by_use_case",
      "deskpro_use": "contextual",
      "notes": "Existing market_metrics has bitget+binance candidates but no scoring yet."
    }
  ]
}
```

## `pro_desk_data_fields.json` — modele cible

```json
{
  "registry_version": "v1",
  "updated_at": "2026-06-05T00:00:00Z",
  "fields": [
    {
      "data_key": "open_interest",
      "data_class": "flow_positioning",
      "priority": "P10",
      "semantic_type": "numeric_metric",
      "unit": "contracts_or_notional_by_source",
      "canonical_contract_candidates": ["market_metrics.v1", "flow_positioning.v1"],
      "source_policy": "multi_source_scored",
      "quality_required": true,
      "resolver_required": true,
      "deskpro_relevance": "high_contextual",
      "current_status": "partial_existing_no_score"
    }
  ]
}
```

## Champs obligatoires par categorie

Chaque categorie P0-P21 doit declarer :

```text
priority
data_class
role
required_for
candidate_contracts
canonical_fields
current_coverage_status
source_policy
freshness_target
deskpro_use
mapping_next_go_required
```

## Status canoniques

```text
complete
partial
absent
legacy_only
declared_not_migrated
source_exists_no_score
source_exists_no_resolver
view_missing
consumer_orphan
producer_path_violation
```

## Regle

Ce modele documentaire prepare les fichiers registry. Les fichiers `modules/data_center/registry/*.json` ne sont pas modifies dans ce child sans validation explicite.
