---
doc_id: GO_OPT_TRADING_DOC_OPS_CHILD_ACTIVE_GOVERNANCE_CLOSEOUT_REVIEW_01_READING
doc_type: chantier_inventory
repo: opt-trading
project: opt-trading
module: governance
go_id: GO_OPT_TRADING_DOC_OPS_CHILD_ACTIVE_GOVERNANCE_CLOSEOUT_REVIEW_01
status: open
lifecycle_stage: inventory
topic_keys:
  - opt-trading
  - governance
  - reading
  - inventory
surface: chantier
source_kind: canonical
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_DOC_OPS_CHILD_ACTIVE_GOVERNANCE_CLOSEOUT_REVIEW_01/02_validation_matrix.md
point_de_reprise: "Tableau de lecture"
updated_at: 2026-04-29
links:
  - docs/chantiers/GO_OPT_TRADING_OBSOLETE_RECLASS_ARCHIVE_AUDIT_01/00_cadrage.md
  - docs/chantiers/GO_OPT_TRADING_ROOT_POLICY_AND_RECLASS_01/00_cadrage.md
  - docs/chantiers/GO_OPT_TRADING_CONTINUITY_INDEX_REALIGNMENT_01/00_cadrage.md
  - docs/chantiers/GO_OPT_TRADING_CANON_STRUCTURE_REALIGNMENT_01/00_cadrage.md
---

# 01_active_go_reading_inventory

## GO lus

| GO | etat index | etat reel lu | decision | justification |
| --- | --- | --- | --- | --- |
| `GO_OPT_TRADING_OBSOLETE_RECLASS_ARCHIVE_AUDIT_01` | `ACTIVE` | audit encore oriente PHASE C puis PHASE D, sans closeout local | `KEEP_ACTIVE` | la matrice canonique et le plan de lots physiques futurs restent a produire |
| `GO_OPT_TRADING_ROOT_POLICY_AND_RECLASS_01` | `ACTIVE` | artefact principal livre mais arbitrage racine encore ouvert sur `bitget_bridge.py` | `KEEP_ACTIVE` | `REPO_ROOT_POLICY.md` documente encore un arbitrage non clos |
| `GO_OPT_TRADING_CONTINUITY_INDEX_REALIGNMENT_01` | `ACTIVE` | cible atteinte, `docs/next/NEXT_GO_CANDIDATES.md` declassé, surfaces `journal*` absentes | `CLOSE_NOW` | le statut actif ne reflete plus qu un manque de propagation et l absence de closeout local |
| `GO_OPT_TRADING_CANON_STRUCTURE_REALIGNMENT_01` | `ACTIVE` | `REPO_SURFACES_MAP.md`, `docs/INDEX.md` et `docs/ARCHITECTURE.md` sont alignes | `CLOSE_NOW` | artefact canonique livre, sans duplication `registry/*`, aucun gap bloquant prouve |

## References de lecture

- `docs/index/GO_INDEX.md`
- `docs/index/GO_CLOSED_INDEX.md`
- `docs/index/GO_PARENT_THREAD_MAP.md`
- `docs/index/ACTIVE_STREAMS.md`
- `docs/index/NEXT_GO_CANDIDATES.md`
- `docs/index/REPRISE.md`
- `docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md`
- `docs/governance/REPO_ROOT_POLICY.md`
- `docs/architecture/REPO_SURFACES_MAP.md`
