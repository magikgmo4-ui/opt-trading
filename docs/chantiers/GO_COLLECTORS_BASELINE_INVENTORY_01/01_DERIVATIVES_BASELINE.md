---
doc_id: GO_COLLECTORS_BASELINE_INVENTORY_01_DERIVATIVES_BASELINE
doc_type: baseline_inventory
repo: opt-trading
project: opt-trading
module: product
go_id: GO_COLLECTORS_BASELINE_INVENTORY_01
status: draft_for_review
lifecycle_stage: child_inventory
parent_go_id: GO_OPT_TRADING_CONSOLIDATION_COLLECTORS_CLUSTER_01
topic_keys:
  - opt-trading
  - collectors
  - derivatives
  - baseline
surface: product
source_kind: canonical_draft
reference_canonique_principale: docs/chantiers/GO_COLLECTORS_BASELINE_INVENTORY_01/01_DERIVATIVES_BASELINE.md
point_de_reprise: "Inventorier wrappers, config et outputs du derivatives_collector."
updated_at: 2026-05-07
links:
  - docs/chantiers/GO_COLLECTORS_BASELINE_INVENTORY_01/00_CADRAGE.md
---

# 01_DERIVATIVES_BASELINE

## 1_WRAPPERS

```text
Wrappers actuels dans modules/derivatives_collector/scripts/ :
- cmd.sh
- menu.sh
- sanity_check.sh
- lifecycle_compat.sh
```

## 2_CONFIG BOUNDARY

```text
Config visible :
- config/env.example

Questions a figer ensuite :
- committed defaults reelles
- overrides machine-local
- env overrides actifs
```

## 3_OUTPUT ARTIFACTS

```text
Outputs historiques confirmes :
- JSON / CSV legacy exports

Outputs famille compatibles ajoutes :
- manifest.json
- status.json
- latest.json
- events.jsonl
- errors.jsonl

Regle doctrinale : conserver les legacy exports, ajouter les artifacts famille sans casse.
```

## 4_RUNTIME FACETS

```text
Code principal :
- app/derivatives_collector.py
- app/lifecycle_compat.py
- app/binance_adapter.py
- app/bitget_adapter.py

Surface historique exposee :
- collect
- sample
- export
- status

Surface lifecycle compatibility :
- lifecycle
- lifecycle-sample
- lifecycle-export
- lifecycle-status
```

## RISKS

- À qualifier.
