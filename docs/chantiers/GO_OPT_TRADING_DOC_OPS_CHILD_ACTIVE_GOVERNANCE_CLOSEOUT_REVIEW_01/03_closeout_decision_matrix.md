---
doc_id: GO_OPT_TRADING_DOC_OPS_CHILD_ACTIVE_GOVERNANCE_CLOSEOUT_REVIEW_01_CLOSEOUT_MATRIX
doc_type: chantier_matrix
repo: opt-trading
project: opt-trading
module: governance
go_id: GO_OPT_TRADING_DOC_OPS_CHILD_ACTIVE_GOVERNANCE_CLOSEOUT_REVIEW_01
status: open
lifecycle_stage: decisions
topic_keys:
  - opt-trading
  - governance
  - decision_matrix
surface: chantier
source_kind: canonical
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_DOC_OPS_CHILD_ACTIVE_GOVERNANCE_CLOSEOUT_REVIEW_01/02_validation_matrix.md
point_de_reprise: "Section Classement"
updated_at: 2026-04-29
links:
  - docs/chantiers/GO_OPT_TRADING_CONTINUITY_INDEX_REALIGNMENT_01/90_closeout.md
  - docs/chantiers/GO_OPT_TRADING_CANON_STRUCTURE_REALIGNMENT_01/90_closeout.md
---

# 03_closeout_decision_matrix

## Classement

### CLOSE_NOW

- `GO_OPT_TRADING_CONTINUITY_INDEX_REALIGNMENT_01`
- `GO_OPT_TRADING_CANON_STRUCTURE_REALIGNMENT_01`

### KEEP_ACTIVE

- `GO_OPT_TRADING_OBSOLETE_RECLASS_ARCHIVE_AUDIT_01`
- `GO_OPT_TRADING_ROOT_POLICY_AND_RECLASS_01`

### DEFER

- aucun

### REVIEW

- aucun

## Condition de patch

- creer les closeouts locaux manquants des 2 GO clos
- retirer les 2 GO clos des surfaces actives
- les ajouter a `GO_CLOSED_INDEX.md`
- laisser `BRANCH_STATE.md` inchange

## RISKS

- À qualifier.
