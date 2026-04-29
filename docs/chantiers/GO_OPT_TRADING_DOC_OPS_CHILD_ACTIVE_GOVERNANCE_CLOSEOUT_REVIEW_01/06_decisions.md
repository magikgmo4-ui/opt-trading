---
doc_id: GO_OPT_TRADING_DOC_OPS_CHILD_ACTIVE_GOVERNANCE_CLOSEOUT_REVIEW_01_DECISIONS
doc_type: chantier_decisions
repo: opt-trading
project: opt-trading
module: governance
go_id: GO_OPT_TRADING_DOC_OPS_CHILD_ACTIVE_GOVERNANCE_CLOSEOUT_REVIEW_01
status: open
lifecycle_stage: decisions
topic_keys:
  - opt-trading
  - governance
  - decisions
  - closeout
surface: chantier
source_kind: canonical
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_DOC_OPS_CHILD_ACTIVE_GOVERNANCE_CLOSEOUT_REVIEW_01/02_validation_matrix.md
point_de_reprise: "Section Decisions"
updated_at: 2026-04-29
links:
  - docs/chantiers/GO_OPT_TRADING_CONTINUITY_INDEX_REALIGNMENT_01/90_closeout.md
  - docs/chantiers/GO_OPT_TRADING_CANON_STRUCTURE_REALIGNMENT_01/90_closeout.md
  - docs/index/GO_INDEX.md
  - docs/index/GO_CLOSED_INDEX.md
---

# 06_decisions

## Decisions

### D1

L etat reel prouve du repo prime sur la persistance d un statut `ACTIVE` dans les index.

### D2

`GO_OPT_TRADING_CONTINUITY_INDEX_REALIGNMENT_01` passe en `CLOSE_NOW`.

Justification :
- `docs/index/*` est coherent a date
- `docs/next/NEXT_GO_CANDIDATES.md` est deja declassé
- les surfaces `journal*` visees par le lot 2 sont absentes
- un closeout local peut etre cree sans ambiguite

### D3

`GO_OPT_TRADING_CANON_STRUCTURE_REALIGNMENT_01` passe en `CLOSE_NOW`.

Justification :
- `docs/architecture/REPO_SURFACES_MAP.md` est l artefact attendu
- `docs/INDEX.md` et `docs/ARCHITECTURE.md` sont realignes
- aucun ecart reel bloquant n est encore porte dans le repo

### D4

`GO_OPT_TRADING_ROOT_POLICY_AND_RECLASS_01` reste `KEEP_ACTIVE`.

Justification :
- `REPO_ROOT_POLICY.md` documente encore un arbitrage racine ouvert sur `bitget_bridge.py`

### D5

`GO_OPT_TRADING_OBSOLETE_RECLASS_ARCHIVE_AUDIT_01` reste `KEEP_ACTIVE`.

Justification :
- la matrice canonique obsolete/archive et le plan de lots futurs ne sont pas encore livres

### D6

`GO_PARENT_THREAD_MAP.md` recoit uniquement un patch de statut sur les 2 GO clos ; sa structure derivee n est pas reouverte.

### D7

`BRANCH_STATE.md` reste hors patch faute d incoherence prouvee.
