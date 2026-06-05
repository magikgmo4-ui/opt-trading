---
doc_id: GO_COLLECTORS_HELPER_EXTRACTION_IMPL_01_CADRAGE
doc_type: cadrage
repo: opt-trading
project: opt-trading
module: product
go_id: GO_COLLECTORS_HELPER_EXTRACTION_IMPL_01
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
reference_canonique_principale: docs/chantiers/GO_COLLECTORS_HELPER_EXTRACTION_IMPL_01/00_CADRAGE.md
point_de_reprise: "Extraire un premier lot de helpers génériques vers collectors_core."
updated_at: 2026-05-07
links:
  - docs/chantiers/GO_COLLECTORS_HELPER_EXTRACTION_CANDIDATES_01/90_CLOSEOUT.md
---

# 00_CADRAGE — GO_COLLECTORS_HELPER_EXTRACTION_IMPL_01

## 1_MASTER_TARGET

Implémenter un premier lot de helper extraction, strictement borné aux utilitaires génériques déjà dupliqués dans `lifecycle_compat.py`.

## 2_LOT RETENU

```text
- build_run_id / now_z / parse_z
- load_json / atomic_write_json / append_jsonl
- ensure_file
- module_relative_path
```

## 12_INVARIANTS

```text
- pas de logique métier dérivés déplacée
- extraction additive et sûre
- aucune sémantique de payload changée
```

## RISKS

- À qualifier.
