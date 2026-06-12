---
doc_id: GO_COLLECTORS_CONFIG_BOUNDARY_ALIGNMENT_01_CADRAGE
doc_type: cadrage
repo: opt-trading
project: opt-trading
module: product
go_id: GO_COLLECTORS_CONFIG_BOUNDARY_ALIGNMENT_01
status: draft_for_review
lifecycle_stage: child_cadrage
parent_go_id: GO_COLLECTORS_ARTIFACT_FAMILY_ALIGNMENT_01
topic_keys:
  - opt-trading
  - collectors
  - config
  - boundary
surface: product
source_kind: canonical_draft
reference_canonique_principale: docs/chantiers/GO_COLLECTORS_CONFIG_BOUNDARY_ALIGNMENT_01/00_CADRAGE.md
point_de_reprise: "Aligner la doctrine de boundary config collectors sans migration disruptive."
updated_at: 2026-05-07
links:
  - docs/COLLECTORS_MIGRATION_MAP_01.md
  - docs/COLLECTORS_FAMILY_DOCTRINE_01.md
---

# 00_CADRAGE — GO_COLLECTORS_CONFIG_BOUNDARY_ALIGNMENT_01

## 1_MASTER_TARGET

Aligner la boundary config de la famille COLLECTORS autour de 4 notions :
- committed defaults
- machine-local overrides
- env overrides
- secrets boundary

## 2_RULE

```text
Documenter d'abord la target boundary.
N'introduire des layers de compatibilite que si necessaire.
Ne pas forcer une migration disruptive en une etape.
```

## 12_INVARIANTS

```text
- docs only
- 0 runtime
- 0 secrets en clair
- 0 migration config executee
```

## RISKS

- À qualifier.
