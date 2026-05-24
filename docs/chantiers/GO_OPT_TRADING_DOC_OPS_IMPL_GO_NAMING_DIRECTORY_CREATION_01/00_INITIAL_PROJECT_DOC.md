---
go_id: GO_OPT_TRADING_DOC_OPS_IMPL_GO_NAMING_DIRECTORY_CREATION_01
doc_type: INITIAL_PROJECT_DOC
repo: opt-trading
project: opt-trading
status: OPEN
updated_at: 2026-05-23
---

# 00_INITIAL_PROJECT_DOC

## 1_MASTER_TARGET
Implement the priority candidate #2 from GO_OPT_TRADING_DOC_OPS_SELECTION_AUTOMATION_PRIORITY_01: GO Naming + Directory Creation.

## 2_INITIAL_PROJECT_DOC
This document.

## 3_INITIAL_NEED
The Doc Ops process requires manual creation of directory structures and initial documentation for every new GO. This is time-consuming and prone to naming inconsistencies.

## 4_MASTER_PROJECT_PLAN
1. Implement `scripts/ai/workers/doc_ops_create_chantier.py`.
2. Implement `tests/ai/workers/test_doc_ops_create_chantier.py`.
3. Provide full project documentation in `docs/chantiers/GO_OPT_TRADING_DOC_OPS_IMPL_GO_NAMING_DIRECTORY_CREATION_01/`.
4. Validate with existing `doc_ops_constraint_check.py`.

## 6_FINAL_TARGET
A functional CLI tool that automates the creation of canonical chantier structures and validates GO_IDs.

## 7_CANONICAL_STATE
- `scripts/ai/workers/doc_ops_create_chantier.py` exists.
- `tests/ai/workers/test_doc_ops_create_chantier.py` exists and passes.
- Canonical documentation is present and follows the naming/structure rules.

## 12_INVARIANTS
- No modification of global indexes.
- No modification of CI workflows.
- No modification of trading/runtime modules.
- GO_ID validation strictly follows the `GO_<SCOPE>_<PRODUCT_OR_SURFACE>_<ROLE>_<OBJECT>_<NN>` pattern.

## 16_TODO
- [x] Initiation
- [ ] Strategy & Implementation
- [ ] Testing
- [ ] Documentation
- [ ] Close Gate

## 17_RESUME_POINT
Initialized project documentation and ready to implement the script.
