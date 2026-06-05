---
doc_id: GO_OPT_TRADING_DOC_OPS_CHILD_ROOT_ARCHIVE_FINAL_ARBITRATION_01_DECISIONS
doc_type: chantier_decisions
repo: opt-trading
project: opt-trading
module: governance
go_id: GO_OPT_TRADING_DOC_OPS_CHILD_ROOT_ARCHIVE_FINAL_ARBITRATION_01
status: open
lifecycle_stage: decisions
topic_keys:
  - opt-trading
  - governance
  - decisions
  - root
  - archive
surface: chantier
source_kind: canonical
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_DOC_OPS_CHILD_ROOT_ARCHIVE_FINAL_ARBITRATION_01/02_validation_matrix.md
point_de_reprise: "Section Decisions"
updated_at: 2026-04-29
links:
  - docs/governance/REPO_ROOT_POLICY.md
  - docs/chantiers/GO_OPT_TRADING_OBSOLETE_RECLASS_ARCHIVE_AUDIT_01/90_closeout.md
  - docs/chantiers/GO_OPT_TRADING_ROOT_POLICY_AND_RECLASS_01/90_closeout.md
---

# 06_decisions

## Decisions

### D1

`GO_OPT_TRADING_ROOT_POLICY_AND_RECLASS_01` passe en `CLOSE_NOW`.

### D2

Le dernier cas d'arbitrage racine est absorbe par une qualification explicite :
- `bitget_bridge.py` devient une exception de compatibilite legacy explicite

### D3

Les metadata Git racine (`.gitignore`, `.gitattributes`) et les bundles ignores locaux sont qualifies dans la politique racine ; ils ne constituent plus un gap documentaire.

### D4

`GO_OPT_TRADING_OBSOLETE_RECLASS_ARCHIVE_AUDIT_01` passe en `CLOSE_NOW`.

### D5

La matrice d'audit et les lots deja executes sont juges suffisants pour fermer le parent sans nouveau move/delete/archive dans ce lot.

### D6

`BRANCH_STATE.md` reste hors patch faute d'incoherence prouvee.

## RISKS

- À qualifier.
