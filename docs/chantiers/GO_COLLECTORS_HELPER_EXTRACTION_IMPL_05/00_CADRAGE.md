---
doc_id: GO_COLLECTORS_HELPER_EXTRACTION_IMPL_05_CADRAGE
doc_type: cadrage
repo: opt-trading
project: opt-trading
module: product
go_id: GO_COLLECTORS_HELPER_EXTRACTION_IMPL_05
status: draft_for_review
lifecycle_stage: child_cadrage
parent_go_id: GO_COLLECTORS_HELPER_EXTRACTION_CANDIDATES_01
topic_keys:
  - opt-trading
  - collectors
  - helper-extraction
  - implementation
surface: product
source_kind: canonical_draft
reference_canonique_principale: docs/chantiers/GO_COLLECTORS_HELPER_EXTRACTION_IMPL_05/00_CADRAGE.md
point_de_reprise: "Extraire les helpers génériques de lecture status et création groupée de répertoires runtime."
updated_at: 2026-05-07
links:
  - docs/chantiers/GO_COLLECTORS_HELPER_EXTRACTION_IMPL_04/90_CLOSEOUT.md
---

# 00_CADRAGE — GO_COLLECTORS_HELPER_EXTRACTION_IMPL_05

## 1_MASTER_TARGET

Extraire les derniers helpers génériques encore dupliqués côté collecteurs spot : lecture `status.json`, rendu texte du status, et création groupée des répertoires runtime.

## 12_INVARIANTS

```text
- pas de changement payload métier
- pas de migration runtime
- helpers génériques seulement
```
