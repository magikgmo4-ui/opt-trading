---
doc_id: GO_COLLECTORS_OPERATOR_SURFACE_ALIGNMENT_01_SURFACE_BASELINE
doc_type: surface_baseline
repo: opt-trading
project: opt-trading
module: product
go_id: GO_COLLECTORS_OPERATOR_SURFACE_ALIGNMENT_01
status: draft_for_review
lifecycle_stage: child_surface_baseline
parent_go_id: GO_COLLECTORS_CONFIG_BOUNDARY_ALIGNMENT_01
topic_keys:
  - opt-trading
  - collectors
  - operator-surface
surface: product
source_kind: canonical_draft
reference_canonique_principale: docs/chantiers/GO_COLLECTORS_OPERATOR_SURFACE_ALIGNMENT_01/01_SURFACE_BASELINE.md
point_de_reprise: "Poser le baseline cmd/sanity/menu/runbook de la famille collectors."
updated_at: 2026-05-07
links:
  - docs/chantiers/GO_COLLECTORS_OPERATOR_SURFACE_ALIGNMENT_01/00_CADRAGE.md
---

# 01_SURFACE_BASELINE

## 1_SURFACE ATTENDUE

```text
Chaque collector devrait converger vers :
- cmd
- sanity
- menu
- runbook/documentation
- install/shortcuts si pertinent
```

## 2_ETAT ACTUEL

```text
derivatives_collector : cmd/menu/sanity/lifecycle_compat
collector_coingecko   : collector_coingecko_cmd/menu/sanity + runbook
collector_binance_spot: collector_binance_spot_cmd/menu/sanity + runbook
marketdata            : facade cmd/menu/sanity
collectors_core       : package support, pas surface operateur principale
```

## 3_GAP

```text
La famille n'est pas incoherente, mais les conventions de noms restent heterogenes.
```

## RISKS

- À qualifier.
