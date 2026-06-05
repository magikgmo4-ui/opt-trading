---
doc_id: GO_COLLECTORS_HELPER_EXTRACTION_IMPL_01_IMPLEMENTATION_NOTES
doc_type: implementation_notes
repo: opt-trading
project: opt-trading
module: product
go_id: GO_COLLECTORS_HELPER_EXTRACTION_IMPL_01
status: draft_for_review
lifecycle_stage: child_implementation_notes
parent_go_id: GO_COLLECTORS_HELPER_EXTRACTION_CANDIDATES_01
topic_keys:
  - opt-trading
  - collectors
  - helper-extraction
  - implementation
surface: product
source_kind: canonical_draft
reference_canonique_principale: docs/chantiers/GO_COLLECTORS_HELPER_EXTRACTION_IMPL_01/01_IMPLEMENTATION_NOTES.md
point_de_reprise: "Tracer les helpers réellement extraits et la compatibilité conservée."
updated_at: 2026-05-07
links:
  - docs/chantiers/GO_COLLECTORS_HELPER_EXTRACTION_IMPL_01/00_CADRAGE.md
---

# 01_IMPLEMENTATION_NOTES

## 1_CHANGEMENTS

```text
collectors_core/files.py
  + ensure_file()

collectors_core/__init__.py
  + export ensure_file

derivatives_collector/app/lifecycle_compat.py
  - retire plusieurs duplications génériques
  + importe les helpers collectors_core

derivatives_collector/scripts/{cmd.sh,lifecycle_compat.sh}
  + export PYTHONPATH vers packages/collectors_core/src
```

## 2_NON CHANGÉ

```text
- aucune logique métier dérivés
- aucun payload métier
- aucun adapter provider-specific
```

## RISKS

- À qualifier.
