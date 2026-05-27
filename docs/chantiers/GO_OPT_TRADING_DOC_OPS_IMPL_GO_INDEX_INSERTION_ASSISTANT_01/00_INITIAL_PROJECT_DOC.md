---
go_id: GO_OPT_TRADING_DOC_OPS_IMPL_GO_INDEX_INSERTION_ASSISTANT_01
doc_type: INITIAL_PROJECT_DOC
repo: opt-trading
project: opt-trading
status: OPEN
updated_at: 2026-05-27
---

# 00_INITIAL_PROJECT_DOC

## 1_MASTER_TARGET
Créer un assistant contrôlé pour préparer ou appliquer l'insertion d'un GO dans GO_INDEX.md.

## 2_INITIAL_PROJECT_DOC
This document.

## 3_INITIAL_NEED
GO_INDEX.md must be updated when new chantiers are created, but manual editing is error-prone and risky. A controlled CLI assistant is needed to prepare, preview, and optionally insert entries safely.

## 4_MASTER_PROJECT_PLAN
- [x] Initiation — chantier skeleton, branch, source analysis
- [x] Implementation — script `doc_ops_go_index_insert.py`
- [x] Implementation — tests `test_doc_ops_go_index_insert.py`
- [x] Validation — pytest, dry-run, constraint check
- [ ] Close Gate — closeout, PR

## 6_FINAL_TARGET
A working CLI tool that reads a chantier's initial doc, generates a GO_INDEX.md entry, previews the diff by default, and writes only with --apply — all without modifying GO_INDEX.md in this PR.

## 7_CANONICAL_STATE
PR #??? opened. Script created. Tests pass. Dry-run validates. GO_INDEX.md unchanged.

## 12_INVARIANTS
- No modification of global indexes.
- No modification of CI workflows.
- No modification of trading/runtime modules.
- GO_INDEX.md not modified in this PR.

## 16_TODO
- [x] Initiation
- [x] Implementation
- [x] Validation
- [ ] Close Gate

## 17_RESUME_POINT
Script and tests created. Chantier docs complete. Ready for validation and PR.
