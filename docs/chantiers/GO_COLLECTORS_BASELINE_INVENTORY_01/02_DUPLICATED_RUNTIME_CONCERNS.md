---
doc_id: GO_COLLECTORS_BASELINE_INVENTORY_01_DUPLICATED_RUNTIME_CONCERNS
doc_type: duplication_inventory
repo: opt-trading
project: opt-trading
module: product
go_id: GO_COLLECTORS_BASELINE_INVENTORY_01
status: draft_for_review
lifecycle_stage: child_duplication_inventory
parent_go_id: GO_OPT_TRADING_CONSOLIDATION_COLLECTORS_CLUSTER_01
topic_keys:
  - opt-trading
  - collectors
  - duplication
surface: product
source_kind: canonical_draft
reference_canonique_principale: docs/chantiers/GO_COLLECTORS_BASELINE_INVENTORY_01/02_DUPLICATED_RUNTIME_CONCERNS.md
point_de_reprise: "Lister les concerns runtime potentiellement dupliques entre derivatives_collector et collectors_core."
updated_at: 2026-05-07
links:
  - docs/chantiers/GO_COLLECTORS_BASELINE_INVENTORY_01/00_CADRAGE.md
  - packages/collectors_core/README.md
---

# 02_DUPLICATED_RUNTIME_CONCERNS

## 1_COLLECTORS_CORE BOUNDARY

```text
collectors_core couvre deja :
- config boundary
- env/secrets resolution
- HTTP policy
- retry / rate limit
- file helpers
- timestamps
- common errors
```

## 2_DUPLICATIONS A VERIFIER COTE DERIVATIVES

```text
A verifier lors d'une extraction selective future :
- gestion config
- wrappers HTTP / retry
- ecriture artifacts status/latest/manifest
- timestamps / run identity
- taxonomy d'erreurs
```

## 3_CE QUI DOIT RESTER SEPARE

```text
- semantics derives
- adapters provider-specific derives
- normalized contracts derives
- downstream expectations derives
```

## 4_DECISION

```text
Le baseline inventory confirme la bonne question :
aligner d'abord vocabulaire, artifacts, config boundary, operator surface.
Pas d'extraction selective automatique a ce stade.
```

## RISKS

- À qualifier.
