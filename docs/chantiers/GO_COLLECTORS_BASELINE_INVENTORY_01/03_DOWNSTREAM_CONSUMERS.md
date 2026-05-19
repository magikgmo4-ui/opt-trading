---
doc_id: GO_COLLECTORS_BASELINE_INVENTORY_01_DOWNSTREAM_CONSUMERS
doc_type: downstream_inventory
repo: opt-trading
project: opt-trading
module: product
go_id: GO_COLLECTORS_BASELINE_INVENTORY_01
status: draft_for_review
lifecycle_stage: child_downstream_inventory
parent_go_id: GO_OPT_TRADING_CONSOLIDATION_COLLECTORS_CLUSTER_01
topic_keys:
  - opt-trading
  - collectors
  - downstream
surface: product
source_kind: canonical_draft
reference_canonique_principale: docs/chantiers/GO_COLLECTORS_BASELINE_INVENTORY_01/03_DOWNSTREAM_CONSUMERS.md
point_de_reprise: "Fixer les consumers downstream a proteger avant toute migration collectors."
updated_at: 2026-05-07
links:
  - docs/chantiers/GO_COLLECTORS_BASELINE_INVENTORY_01/00_CADRAGE.md
---

# 03_DOWNSTREAM_CONSUMERS

## 1_CONSUMERS A PROTEGER

```text
Consumers explicitement mentionnes par README / doctrine :
- Risk Engine
- Strategy
- downstream consumers des exports JSON / CSV legacy
```

## 2_CONSUMERS INDIRECTS A VERIFIER AU GO SUIVANT

```text
- docs et runbooks qui supposent les noms d'artefacts actuels
- scripts shell qui supposent les sorties derivatives actuelles
- index / dashboards eventuels consommant latest/status
```

## 3_REGLE DE PROTECTION

```text
Avant toute migration runtime future :
- aucun consumer aval ne doit perdre ses legacy outputs
- toute nouvelle doctrine artifact doit etre additive
- tout changement de nom de fichier doit etre mappe puis rollbackable
```
