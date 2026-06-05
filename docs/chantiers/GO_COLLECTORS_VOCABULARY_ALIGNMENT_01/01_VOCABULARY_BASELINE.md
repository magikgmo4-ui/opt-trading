---
doc_id: GO_COLLECTORS_VOCABULARY_ALIGNMENT_01_VOCABULARY_BASELINE
doc_type: vocabulary_baseline
repo: opt-trading
project: opt-trading
module: product
go_id: GO_COLLECTORS_VOCABULARY_ALIGNMENT_01
status: draft_for_review
lifecycle_stage: child_baseline
parent_go_id: GO_COLLECTORS_BASELINE_INVENTORY_01
topic_keys:
  - opt-trading
  - collectors
  - vocabulary
surface: product
source_kind: canonical_draft
reference_canonique_principale: docs/chantiers/GO_COLLECTORS_VOCABULARY_ALIGNMENT_01/01_VOCABULARY_BASELINE.md
point_de_reprise: "Poser le baseline vocabulary actuel cote derives et cote spot."
updated_at: 2026-05-07
links:
  - docs/chantiers/GO_COLLECTORS_VOCABULARY_ALIGNMENT_01/00_CADRAGE.md
---

# 01_VOCABULARY_BASELINE

## 1_FAMILY TERMS DEJA GELÉS

```text
Artifacts famille :
- manifest.json
- status.json
- latest.json
- events.jsonl
- errors.jsonl

Boundaries famille :
- config boundary
- env overrides
- local overrides
- HTTP policy
- operator surface : cmd / sanity / menu / runbook
```

## 2_A ALIGNER ENTRE DERIVES ET SPOT

```text
- module_id
- provider_id
- run_id
- generated_at / collected_at / written_at
- state
- freshness
- error_code / error_class / error_stage
```

## 3_NE PAS ALIGNER

```text
- semantics derives vs spot
- payload schema derives vs spot
- provider endpoint details
```

## RISKS

- À qualifier.
